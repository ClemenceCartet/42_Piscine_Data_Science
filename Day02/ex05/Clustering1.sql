SELECT user_id, COUNT(month) as nb_months, MIN(month) as min_month, MAX(month) as max_month
FROM
	(SELECT date_trunc('month', event_time) as month, user_id
	FROM customers.customersv3
	WHERE event_type = 'purchase'
	GROUP BY date_trunc('month', event_time), user_id
	)
GROUP BY user_id
ORDER BY user_id;