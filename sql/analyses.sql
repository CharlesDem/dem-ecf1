--------------------------------------------------------------------------------------------
-- Une requête d'agrégation simple

SELECT COUNT(*) AS total_tags
FROM tags; --136

--------------------------------------------------------------------------------------------
-- Une requête avec jointure

SELECT t.libelle
FROM quote_tags qt
JOIN tags t ON qt.tag_id = t.tag_id
WHERE qt.quote_id = 1; -- change, deep-thoughts, thinking, world

--------------------------------------------------------------------------------------------
-- Une requête avec fonction de fenêtrage (window function)
--overkill

SELECT *
FROM (
    SELECT
        quote_id,
        text_content,
        last_scrap_version,
        author_id,
        ROW_NUMBER() OVER (
            PARTITION BY text_content
            ORDER BY last_scrap_version DESC
        ) AS rn
    FROM quotes
) sub
WHERE rn = 1; -- devrait retourner les quotes qui ont la plus haute last_scrap_version

--------------------------------------------------------------------------------------------
-- Une requête de classement (top N)

SELECT q.quote_id, q.text_content, COUNT(qt.tag_id) AS tag_count
FROM quotes q
LEFT JOIN quote_tags qt ON q.quote_id = qt.quote_id
GROUP BY q.quote_id, q.text_content
ORDER BY tag_count DESC
LIMIT 3; -- les 3 quotes avec le plus de tags

--------------------------------------------------------------------------------------------
-- Une requête croisant au moins 2 sources de données

INSERT INTO sells (book_id, book_store_id)
VALUES (1, 1); --données nons croisées nativement, on triche un peu

SELECT DISTINCT bs.name -- librairie qui ven d au moins un bouquin
FROM book_stores bs
JOIN sells s ON bs.book_store_id = s.book_store_id; -- Librairie du marais