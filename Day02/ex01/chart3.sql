WITH daily_sums AS (
	SELECT date_trunc('day', event_time) AS day, SUM(price) AS sum_per_user
	FROM customers.customersv3
	WHERE event_type = 'purchase'
	GROUP BY date_trunc('day', event_time), user_id
	)
SELECT day, AVG(sum_per_user) AS average_purchase_per_user
FROM daily_sums
GROUP BY day;