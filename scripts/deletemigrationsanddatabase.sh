#!/bin/bash
echo ""
echo "This will delete all migrations history and all database data. Proceed? (y/n)"
read -r confirmation

if [[ "$confirmation" != "y" ]]; then
  echo "Operation canceled."
  exit 0
fi

rm -rf pg
rm -rf backend/bookingandbilling/migrations/0*.py