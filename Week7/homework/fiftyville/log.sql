-- Keep a log of any SQL queries you execute as you solve the mystery.
-- theft took place on July 28, 2023 and it took place on Humphrey Street

-- understanding what the tables mean
SELECT * FROM airports LIMIT 5;
SELECT * FROM atm_transactions LIMIT 5;
SELECT * FROM bakery_security_logs LIMIT 5;
SELECT * FROM bank_accounts LIMIT 5;
SELECT * FROM crime_scene_reports LIMIT 5;

--searching for the description of the crime in the crime_scene_reports
SELECT * FROM crime_scene_reports WHERE year = 2023 AND month = 7 AND day = 28;
-- the crime took place at 10:15 am

--looking up the interviews
.schema interviews
SELECT * FROM interviews WHERE year = 2023 AND month = 7 AND day = 28;
--the names of witnesses are Ruth, Eugene, and Raymond
-- don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.
-- As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
-- The thief then asked the person on the other end of the phone to purchase the flight ticket.
-- Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
-- If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.


--focusing on 10 minutes within theft
--finding names of people that exited the bakery lot within the given time frame
SELECT * FROM people WHERE license_plate IN
    (SELECT license_plate FROM bakery_security_logs WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25);


--focusing on the earliest flight, JULY 29TH 2023, from Fiftyville where?
.schema airports

--checking the origin is Fiftyville
SELECT full_name FROM airports WHERE id IN
    (SELECT origin_airport_id FROM flights WHERE year = 2023 AND month = 7 AND day = 29 ORDER BY hour ASC LIMIT 10);

--checking the earliest flight from Fiftyville and its destination
SELECT * FROM airports JOIN flights ON airports.id = flights.destination_airport_id
WHERE year = 2023 AND month = 7 AND day = 29 ORDER BY hour ASC LIMIT 1;
-- this is New York City


-- focusing on the overlap in the flights, passengers and people who drove out of bakery lot
SELECT name FROM people WHERE passport_number IN
    (SELECT passport_number FROM passengers WHERE flight_id IN
        (SELECT id FROM flights WHERE year = 2023 AND month = 7 AND day = 29 ORDER BY hour ASC LIMIT 1))
AND license_plate IN
    (SELECT license_plate FROM bakery_security_logs WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25);
-- with this query we narrowed it down to 4 names: Sofia, Luca, Kelsey, Bruce

-- the thief was also at the ATM "I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money"
SELECT name FROM people WHERE id IN
    (SELECT person_id FROM bank_accounts WHERE account_number IN
        (SELECT account_number FROM atm_transactions WHERE year = 2023 AND month = 7 AND day = 28
        AND transaction_type = 'withdraw' AND atm_location = 'Leggett Street'));

-- combining the queries to find the name of the person who took the flight, exited the bakery lot, and withdrew money
SELECT name FROM people WHERE passport_number IN
    (SELECT passport_number FROM passengers WHERE flight_id IN
        (SELECT id FROM flights WHERE year = 2023 AND month = 7 AND day = 29 ORDER BY hour ASC LIMIT 1))
AND license_plate IN
    (SELECT license_plate FROM bakery_security_logs WHERE year = 2023 AND month = 7
    AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25)
AND id IN
    (SELECT person_id FROM bank_accounts WHERE account_number IN
        (SELECT account_number FROM atm_transactions WHERE year = 2023 AND month = 7 AND day = 28
        AND transaction_type = 'withdraw' AND atm_location = 'Leggett Street'));
-- only two people left after this query - Luca and Bruce


-- tracing the phone calls
SELECT * FROM phone_calls WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60;

SELECT name FROM people WHERE phone_number IN
    (SELECT caller FROM phone_calls WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60);

-- combining queries with the previous one (all together with phonecalls)
SELECT name FROM people WHERE passport_number IN
    (SELECT passport_number FROM passengers WHERE flight_id IN
        (SELECT id FROM flights WHERE year = 2023 AND month = 7 AND day = 29 ORDER BY hour ASC LIMIT 1))
AND license_plate IN
    (SELECT license_plate FROM bakery_security_logs WHERE year = 2023 AND month = 7
    AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25)
AND id IN
    (SELECT person_id FROM bank_accounts WHERE account_number IN
        (SELECT account_number FROM atm_transactions WHERE year = 2023 AND month = 7 AND day = 28
        AND transaction_type = 'withdraw' AND atm_location = 'Leggett Street'))
AND phone_number IN
    (SELECT caller FROM phone_calls WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60);
-- the thief is Bruce!

-- finding out the name of the accomplice
SELECT name FROM people JOIN phone_calls ON people.phone_number = phone_calls.receiver
WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60 AND caller IN
    (SELECT phone_number FROM people WHERE passport_number IN
            (SELECT passport_number FROM passengers WHERE flight_id IN
                (SELECT id FROM flights WHERE year = 2023 AND month = 7 AND day = 29 ORDER BY hour ASC LIMIT 1))
        AND license_plate IN
            (SELECT license_plate FROM bakery_security_logs WHERE year = 2023 AND month = 7
            AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25)
        AND id IN
            (SELECT person_id FROM bank_accounts WHERE account_number IN
                (SELECT account_number FROM atm_transactions WHERE year = 2023 AND month = 7 AND day = 28
                AND transaction_type = 'withdraw' AND atm_location = 'Leggett Street'))
        AND phone_number IN
            (SELECT caller FROM phone_calls WHERE year = 2023 AND month = 7 AND day = 28 AND duration < 60));
-- Robin is the accomplice!
