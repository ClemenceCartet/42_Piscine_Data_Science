SELECT user_id, COUNT(month) as nb_months, MIN(month) as min_month
FROM
	(SELECT EXTRACT(MONTH FROM event_time) as month, user_id
	FROM customers.customersv3
	WHERE event_type = 'purchase'
	GROUP BY EXTRACT(MONTH FROM event_time), user_id
	)
GROUP BY user_id;