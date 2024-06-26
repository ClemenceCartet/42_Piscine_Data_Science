SELECT user_id, COUNT(month) as nb_months, SUM(total_price) as total_prices
FROM
	(SELECT user_id, SUM(price) as total_price, date_trunc('month', event_time) as month
	FROM customers.customersv3
	WHERE event_type = 'purchase'
	GROUP BY date_trunc('month', event_time), user_id
	)
GROUP BY user_id
ORDER BY user_id;