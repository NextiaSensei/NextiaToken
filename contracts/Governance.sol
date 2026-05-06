// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Governance is Ownable {
    enum ProposalState { Pending, Active, Defeated, Succeeded, Executed }

    struct Proposal {
        address proposer;
        string title;
        uint256 startBlock;
        uint256 endBlock;
        uint256 forVotes;
        uint256 againstVotes;
        bool executed;
    }

    struct Receipt {
        bool hasVoted;
        uint8 support;
        uint256 votes;
    }

    IERC20 public nxtToken;
    uint256 public proposalCount;
    uint256 public votingPeriod = 50400;
    
    mapping(uint256 => Proposal) public proposals;
    mapping(uint256 => mapping(address => Receipt)) public receipts;

    event ProposalCreated(uint256 indexed id, address indexed proposer, uint256 startBlock, uint256 endBlock);
    event VoteCast(address indexed voter, uint256 indexed proposalId, uint8 support, uint256 votes);
    event ProposalExecuted(uint256 indexed id);

    constructor(address _nxtTokenAddress, address _initialOwner) Ownable(_initialOwner) {
        require(_nxtTokenAddress != address(0), "Invalid token");
        nxtToken = IERC20(_nxtTokenAddress);
    }

    function proposeGovernanceChange(string memory title) external returns (uint256) {
        require(nxtToken.balanceOf(msg.sender) >= 1000 * 1e18, "Insufficient NXT");

        uint256 proposalId = proposalCount;
        uint256 startBlock = block.number + 1;
        uint256 endBlock = startBlock + votingPeriod;

        proposals[proposalId] = Proposal({
            proposer: msg.sender,
            title: title,
            startBlock: startBlock,
            endBlock: endBlock,
            forVotes: 0,
            againstVotes: 0,
            executed: false
        });

        proposalCount++;
        emit ProposalCreated(proposalId, msg.sender, startBlock, endBlock);
        return proposalId;
    }

    function castVote(uint256 proposalId, uint8 support) external {
        require(proposalId < proposalCount, "Invalid proposal");
        require(block.number >= proposals[proposalId].startBlock, "Voting not started");
        require(block.number <= proposals[proposalId].endBlock, "Voting ended");
        require(!receipts[proposalId][msg.sender].hasVoted, "Already voted");

        uint256 votes = nxtToken.balanceOf(msg.sender);
        require(votes > 0, "No voting power");

        receipts[proposalId][msg.sender] = Receipt({
            hasVoted: true,
            support: support,
            votes: votes
        });

        if (support == 0) {
            proposals[proposalId].againstVotes += votes;
        } else {
            proposals[proposalId].forVotes += votes;
        }

        emit VoteCast(msg.sender, proposalId, support, votes);
    }

    function executeProposal(uint256 proposalId) external onlyOwner {
        require(proposalId < proposalCount, "Invalid proposal");
        require(block.number > proposals[proposalId].endBlock, "Voting active");
        require(proposals[proposalId].forVotes > proposals[proposalId].againstVotes, "Proposal lost");
        require(!proposals[proposalId].executed, "Already executed");

        proposals[proposalId].executed = true;
        emit ProposalExecuted(proposalId);
    }

    function getProposalInfo(uint256 proposalId) external view returns (
        address, string memory, uint256, uint256, uint256
    ) {
        Proposal memory p = proposals[proposalId];
        return (p.proposer, p.title, p.forVotes, p.againstVotes, 
                p.executed ? 1 : 0);
    }
}
