script_dir="$(cd "$(dirname "$0")" && pwd)"; folder="$script_dir/../data/queries"
for file in "$folder"/*; do
  
  sqlite3 -header -csv db.sqlite3 < "$file" > temp.csv
  csv2md temp.csv > $folder/../reports/$(basename "$file" .sql).md
  rm temp.csv
done