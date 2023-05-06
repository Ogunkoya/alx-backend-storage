CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE user_cursor CURSOR FOR SELECT id FROM users;
    DECLARE continue_handler BOOLEAN DEFAULT TRUE;
    DECLARE user_id INT;
    DECLARE weighted_sum FLOAT;
    DECLARE total_weight FLOAT;
    DECLARE avg_weighted_score FLOAT;
    
    CREATE TEMPORARY TABLE temp_weighted_scores (
        user_id INT,
        weighted_score FLOAT
    );
    
    OPEN user_cursor;
    SET continue_handler = TRUE;
    
    user_loop: LOOP
        FETCH user_cursor INTO user_id;
        IF continue_handler = FALSE THEN
            LEAVE user_loop;
        END IF;
        
        SELECT SUM(score * weight) INTO weighted_sum, SUM(weight) INTO total_weight
        FROM corrections
        WHERE user_id = user_id;
        
        IF total_weight IS NOT NULL AND total_weight <> 0 THEN
            SET avg_weighted_score = weighted_sum / total_weight;
            INSERT INTO temp_weighted_scores(user_id, weighted_score) VALUES (user_id, avg_weighted_score);
        END IF;
    END LOOP;
    
    CLOSE user_cursor;
    
    DELETE FROM average_weighted_scores;
    
    INSERT INTO average_weighted_scores(user_id, weighted_score)
    SELECT user_id, weighted_score FROM temp_weighted_scores;
    
    DROP TEMPORARY TABLE IF EXISTS temp_weighted_scores;
END;