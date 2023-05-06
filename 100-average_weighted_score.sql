CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE total_score FLOAT;
    DECLARE total_weight FLOAT;
    DECLARE average_score FLOAT;

    SELECT SUM(score * weight) INTO total_score
    FROM corrections
    WHERE user_id = user_id;

    SELECT SUM(weight) INTO total_weight
    FROM corrections
    WHERE user_id = user_id;

    IF total_weight IS NULL OR total_weight = 0 THEN
        SET average_score = 0;
    ELSE
        SET average_score = total_score / total_weight;
    END IF;

    UPDATE users
    SET weighted_avg_score = average_score
    WHERE id = user_id;
END;