SELECT
	COUNT(product_id),
	AVG(price) AS mean,
	PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY price) AS median,
	PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY price) AS q1,
	PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY price) AS q3,
	MIN(price) AS min,
	MAX(price) AS max,
	SQRT(VARIANCE(price)) AS std
FROM customers.customersv3
WHERE event_type = 'purchase';