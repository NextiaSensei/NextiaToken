// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Staking is Ownable {
    struct StakingInfo {
        uint256 amount;
        uint256 startTime;
        uint256 lastRewardTime;
        uint256 rewards;
    }

    IERC20 public nxtToken;

    // 🔹 APY ≈ 20% anual
    // 0.20 / 31,536,000 ≈ 6.341958396e-9
    // En formato 1e18:
    uint256 public rewardRatePerSecond = 6341958396;

    uint256 public totalStaked;
    uint256 public rewardPool;

    mapping(address => StakingInfo) public stakingInfo;

    event Deposited(address indexed user, uint256 amount);
    event Withdrawn(address indexed user, uint256 amount);
    event RewardsClaimed(address indexed user, uint256 amount);
    event RewardsFunded(uint256 amount);

    constructor(address _nxtTokenAddress, address _initialOwner)
        Ownable(_initialOwner)
    {
        require(_nxtTokenAddress != address(0), "Invalid token");
        nxtToken = IERC20(_nxtTokenAddress);
    }

    // =========================
    // 🔹 STAKING
    // =========================

    function deposit(uint256 amount) external {
        require(amount > 0, "Amount > 0");
        require(nxtToken.transferFrom(msg.sender, address(this), amount), "Transfer failed");

        if (stakingInfo[msg.sender].amount > 0) {
            _calculateRewards(msg.sender);
        }

        stakingInfo[msg.sender].amount += amount;
        stakingInfo[msg.sender].startTime = block.timestamp;
        stakingInfo[msg.sender].lastRewardTime = block.timestamp;

        totalStaked += amount;

        emit Deposited(msg.sender, amount);
    }

    function withdraw(uint256 amount) external {
        require(amount > 0, "Amount > 0");
        require(stakingInfo[msg.sender].amount >= amount, "Insufficient");

        _calculateRewards(msg.sender);

        stakingInfo[msg.sender].amount -= amount;
        totalStaked -= amount;

        require(nxtToken.transfer(msg.sender, amount), "Transfer failed");

        emit Withdrawn(msg.sender, amount);
    }

    function withdrawAll() external {
        StakingInfo storage user = stakingInfo[msg.sender];
        require(user.amount > 0, "Nothing staked");

        _calculateRewards(msg.sender);

        uint256 stakedAmount = user.amount;
        uint256 rewards = user.rewards;

        // 🔒 Validación pool
        require(rewardPool >= rewards, "Insufficient reward pool");
        rewardPool -= rewards;

        user.amount = 0;
        user.rewards = 0;
        totalStaked -= stakedAmount;

        uint256 totalTransfer = stakedAmount + rewards;
        require(nxtToken.transfer(msg.sender, totalTransfer), "Transfer failed");

        emit Withdrawn(msg.sender, stakedAmount);
        if (rewards > 0) {
            emit RewardsClaimed(msg.sender, rewards);
        }
    }

    function claimRewards() external {
        _calculateRewards(msg.sender);

        uint256 rewards = stakingInfo[msg.sender].rewards;
        require(rewards > 0, "No rewards");

        // 🔒 Validación pool
        require(rewardPool >= rewards, "Insufficient reward pool");
        rewardPool -= rewards;

        stakingInfo[msg.sender].rewards = 0;
        stakingInfo[msg.sender].lastRewardTime = block.timestamp;

        require(nxtToken.transfer(msg.sender, rewards), "Transfer failed");

        emit RewardsClaimed(msg.sender, rewards);
    }

    // =========================
    // 🔹 REWARDS
    // =========================

    function fundRewards(uint256 amount) external onlyOwner {
        require(amount > 0, "Amount > 0");
        require(nxtToken.transferFrom(msg.sender, address(this), amount), "Transfer failed");

        rewardPool += amount;

        emit RewardsFunded(amount);
    }

    function _calculateRewards(address userAddr) internal {
        StakingInfo storage info = stakingInfo[userAddr];

        if (info.amount == 0) return;

        uint256 timeElapsed = block.timestamp - info.lastRewardTime;
        if (timeElapsed == 0) return;

        uint256 newRewards = (timeElapsed * info.amount * rewardRatePerSecond) / 1e18;

        info.rewards += newRewards;
        info.lastRewardTime = block.timestamp;
    }

    // =========================
    // 🔹 VIEW FUNCTIONS
    // =========================

    function getPendingRewards(address userAddr) external view returns (uint256) {
        StakingInfo storage info = stakingInfo[userAddr];

        if (info.amount == 0) return info.rewards;

        uint256 timeElapsed = block.timestamp - info.lastRewardTime;
        uint256 newRewards = (timeElapsed * info.amount * rewardRatePerSecond) / 1e18;

        return info.rewards + newRewards;
    }

    function getStakedAmount(address userAddr) external view returns (uint256) {
        return stakingInfo[userAddr].amount;
    }

    // =========================
    // 🔹 ADMIN
    // =========================

    function setRewardRate(uint256 newRate) external onlyOwner {
        rewardRatePerSecond = newRate;
    }
}
