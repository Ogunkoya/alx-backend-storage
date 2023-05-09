CREATE FUNCTION SafeDiv (a INT, b INT)
RETURNS FLOAT
BEGIN
    DECLARE result FLOAT;

    IF b != 0 THEN
        SET result = a / b;
    ELSE
        SET result = 0;
    END IF;

    RETURN result;
END;