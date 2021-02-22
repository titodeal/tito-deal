#!/bin/bash

# HOST=192.168.88.167
# PORT=5432
# DATABASE=test_db
# OWNER=titodeal
HOST=$1
PORT=$2
DATABASE=$3
OWNER=$4
 
check_sql_server(){

# echo -e "\n=> Checking server access...\n\tHost: '$HOST'\n\tPort: '$PORT'"
    cat <<- _EOF_
=> Checking server access for:
    HOST: "$HOST"
    PORT: "$PORT"
    DATABASE: "$DATABASE"
    OWNER: "$OWNER"
_EOF_

    if [[ 
        ! $(psql -h "$HOST" \
                 -p "$PORT" \
                 -U "$OWNER" \
                 -l \
        | wc -l) -gt 0 ]]; then
        return 1
    fi
}

check_db () {

    local DATABASE="${1,,}" # to lowercase

    if [ -z $DATABASE ]; then
        echo "!=> Database name argument not specified" >&2
        return 1
    fi
    echo "=> Checking DATABASE $DATABASE"
    if [[
            $(psql -h "$HOST" \
                     -p "$PORT" \
                     -U "$OWNER" -l \
            | grep -w $DATABASE \
            | wc -l) -eq 1 
       ]]; then
        return 0
    fi

    # if the database not exists it will be created.
    echo "=> Creating '$DATABASE' database..."
    psql -h "$HOST" -p "$PORT" -U "$OWNER" -c "CREATE DATABASE $DATABASE"
    if [[ $? == 0 ]]; then
        echo "=> Database '$1' have been created successfull"
        return 0
    else 
        return 1
    fi    
}

# psql -h "$HOST" -p "$PORT" -U "$OWNER" -l | grep titoTst | wc -l 
check_sql_server
if [[ ! $? == 0 ]]; then exit 1; else echo "OK"; fi
check_db $DATABASE
if [[ ! $? == 0 ]]; then exit 1; else echo "OK"; fi

echo "=>Initilize database tablse..."
psql -h "$HOST" -p "$PORT" -U "$OWNER" -d $DATABASE -f "./SQL_tables.sql"

exit 0
