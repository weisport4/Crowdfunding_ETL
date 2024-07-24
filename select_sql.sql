-- The UNION ALL including the table_name as a column prior to the count will give us a list of all tables and their respective counts

SELECT 
    'Campaign' AS table_name, 
    COUNT(*) AS table_count 
FROM 
    campaign
UNION ALL
SELECT 
    'Category' AS table_name, 
    COUNT(*) AS table_count 
FROM 
    category
UNION ALL
SELECT 
    'Subcategory' AS table_name, 
    COUNT(*) AS table_count 
FROM 
    subcategory
UNION ALL
SELECT 
    'Contact' AS table_name, 
    COUNT(*) AS table_count 
FROM 
    contact
;