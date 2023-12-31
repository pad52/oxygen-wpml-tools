<?php

// Read database configuration from wp-config.php
function read_db_config($filename) {
    $config = array();
    $lines = file($filename, FILE_IGNORE_NEW_LINES);
    foreach ($lines as $line) {
        if (preg_match("/define\(\s*'([^']+)'\s*,\s*'([^']+)'\s*\);/", $line, $matches)) {
            $config[$matches[1]] = $matches[2];
        }
    }
    return $config;
}

// Connect to the database
function connect_to_db($config) {
    $connection = new mysqli(
        $config['DB_HOST'],
        $config['DB_USER'],
        $config['DB_PASSWORD'],
        $config['DB_NAME']
    );

    if ($connection->connect_error) {
        die("Connection failed: " . $connection->connect_error);
    }
    
    return $connection;
}

// Execute the SQL query and create separate files for each row
function execute_query_and_create_files($connection) {
    $query = "
    SELECT jkh_postmeta.post_id AS postId, 
    jkh_postmeta.meta_value AS jsonValue, 
    jkh_posts.post_type as type,
    jkh_posts.post_name AS slug,
    jkh_icl_translations.language_code AS lang
    FROM jkh_postmeta 
    INNER JOIN jkh_posts 
    ON jkh_posts.ID = jkh_postmeta.post_id
    INNER JOIN jkh_icl_translations 
    ON jkh_postmeta.post_id = jkh_icl_translations.element_id
    WHERE jkh_postmeta.meta_key LIKE 'ct_builder_json' AND 
    jkh_postmeta.meta_value LIKE '%{\"%' AND
    (jkh_posts.post_type LIKE 'page' OR 
    jkh_posts.post_type LIKE 'ct_template')
    ORDER BY jkh_postmeta.post_id ASC";

    $result = $connection->query($query);

    while ($row = $result->fetch_assoc()) {
        $lang = $row['lang'];
        $slug = $row['slug'];
        $type = $row['type'];
        $data = $row['jsonValue'];
        $filename = "jsons/$lang/$lang-$type-$slug.json";
        file_put_contents($filename, $data);
        
    }
}

$wp_config_file = $argv[1];
$db_config = read_db_config($wp_config_file);
$db_connection = connect_to_db($db_config);
execute_query_and_create_files($db_connection);
$db_connection->close();
echo "Query results written to files with desired names.\n";
