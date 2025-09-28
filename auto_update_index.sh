
ROOT="$HOME/proyectos/nextia"
cd "$ROOT"
while inotifywait -r -e modify,create,delete --exclude 'project_index\.(csv|md|html)' "$ROOT"; do
  python3 "$ROOT/scan_nextia.py"
done
