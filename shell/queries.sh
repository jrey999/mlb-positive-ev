script_dir="$(cd "$(dirname "$0")" && pwd)"; folder="$script_dir/../data/queries"
for file in "$folder"/*; do
  
  sqlite3 -header -csv db.sqlite3 < "$file" > $(basename "$file" .sql).csv
  torst $(basename "$file" .sql).csv -o $folder/../reports/
  rm $(basename "$file" .sql).csv
done