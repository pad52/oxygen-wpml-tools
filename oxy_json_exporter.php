<?php

// Read database configuration from WP CLI
function read_db_config() {
    $db_config = array();

    // Execute WP CLI command to get database configuration
    exec("wp config get DB_HOST", $output, $return_var);
    $db_config['DB_HOST'] = trim(implode("", $output));
    unset($output);
    
    exec("wp config get DB_USER", $output, $return_var);
    $db_config['DB_USER'] = trim(implode("", $output));
    unset($output);
    
    exec("wp config get DB_PASSWORD", $output, $return_var);
    $db_config['DB_PASSWORD'] = trim(implode("", $output));
    unset($output);
    
    exec("wp config get DB_NAME", $output, $return_var);
    $db_config['DB_NAME'] = trim(implode("", $output));
    unset($output);
    
    // Execute WP CLI command to get table prefix
    exec("wp config get table_prefix", $output, $return_var);
    $table_prefix = trim(implode("", $output));
    if ($table_prefix !== '') {
        $db_config['table_prefix'] = $table_prefix;
    } else {
        // If table prefix is not defined, set a default value
        $db_config['table_prefix'] = 'wp_'; // You can change this default value as per your setup
    }

    return $db_config;
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
function execute_query_and_create_files($connection, $table_prefix) {
    $query = "SELECT ".$table_prefix."postmeta.post_id AS postId, 
    ".$table_prefix."postmeta.meta_value AS jsonValue, 
    ".$table_prefix."posts.post_type as type,
    ".$table_prefix."posts.post_name AS slug,
    ".$table_prefix."icl_translations.language_code AS lang,
    ".$table_prefix."icl_translations.trid as trid,
    ".$table_prefix."icl_translations.source_language_code as slang
    FROM ".$table_prefix."postmeta 
    INNER JOIN ".$table_prefix."posts 
    ON ".$table_prefix."posts.ID = ".$table_prefix."postmeta.post_id
    INNER JOIN ".$table_prefix."icl_translations 
    ON ".$table_prefix."postmeta.post_id = ".$table_prefix."icl_translations.element_id
    WHERE ".$table_prefix."postmeta.meta_key LIKE 'ct_builder_json' AND 
    ".$table_prefix."postmeta.meta_value LIKE '%{\"%' AND
    (".$table_prefix."posts.post_type LIKE 'page' OR 
    ".$table_prefix."posts.post_type LIKE 'ct_template')
    ORDER BY ".$table_prefix."postmeta.post_id ASC";

    echo $query;
    
    $result = $connection->query($query);

    while ($row = $result->fetch_assoc()) {
        $id = $row['postId'];
        $slang = $row['slang'];
        $trid = $row['trid'];
        $lang = $row['lang'];
        $slug = $row['slug'];
        $type = $row['type'];
        $data = $row['jsonValue'];
        $filename = "jsons/$lang-$type.$slug.$id.$slang.$trid.json";
        file_put_contents($filename, $data);
        
    }
}

// Main execution starts here

$db_config = read_db_config();
$db_connection = connect_to_db($db_config);
$table_prefix = $db_config['table_prefix'];
execute_query_and_create_files($db_connection, $table_prefix);
$db_connection->close();
echo "Query results written to files with desired names.\n";

?>
