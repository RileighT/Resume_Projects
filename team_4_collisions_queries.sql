USE accidents_table;

/* Query 1 View with multiple tables using join */
CREATE VIEW accidents_info AS
SELECT `Collision_ID (PK)`, `Crash_Date`, `Crash_Time`, `Contributing_Factor`
FROM `accidents_table`
JOIN `factors_accidents_joint` USING(`Collision_ID (PK)`)
JOIN `contributing_factors_table` USING(`Factor_ID (PK)`);

/* Query 2 View with multiples tables, filtering, and aggregation */
CREATE VIEW damaged_vehicles AS
SELECT `Vehicle_Make`,COUNT(`Vehicle_ID (PK)`) AS `Total_Damaged_Vehicles`
FROM `vehicle_table`
JOIN `vehicle_accidents_joint` USING (`Vehicle_ID (PK)`)
JOIN `vehicle_damage_type_table` USING (`Damage_ID (PK)`)
WHERE `Vehicle_Damage` LIKE '%Front%'
GROUP BY `Vehicle_Make`;

/* Query 3 View that uses aggregation and filtering*/
CREATE VIEW accident_count_by_date AS
SELECT `Crash_Date`, COUNT(`Collision_ID (PK)`) AS `Num_Accidents`
FROM `accidents_table`
GROUP BY `Crash_Date`
HAVING COUNT(`Collision_ID (PK)`) > 1;

/* Query 4 View that uses link table and the source tables*/
CREATE VIEW public_property_damage_info AS
SELECT `Public_Property_Damage_ID (PK)`, `Collision_ID (PK)`, `Public_Property_Damage`
FROM `public_property_damage`
JOIN `public_accidents_joint` USING(`Public_Property_Damage_ID (PK)`)
JOIN `accidents_table` USING(`Collision_ID (PK)`);

/* Query 5 View that uses a Subquery*/
CREATE VIEW high_risk_drivers AS
SELECT 
    dt.`Driver_ID (PK)` AS Driver_ID_PK,
    dt.`Driver_Sex`,
    dt.`Driver_Liscence_Status`,
    vt.`Vehicle_ID (PK)` AS Vehicle_ID_PK,
    vt.`State_Registration`,
    at.`Collision_ID (PK)` AS Collision_ID_PK,
    at.`Accident_Identifier`,
    at.`Crash_Date`,
    at.`Pre_Crash`,
    at.`Crash_Time`
FROM  `driver_table` dt
JOIN  `vehicle_table` vt ON dt.`Driver_ID (PK)` = vt.`Driver_ID (FK)`
JOIN  `vehicle_accidents_joint` vaj ON vt.`Vehicle_ID (PK)` = vaj.`Vehicle_ID (PK)`
JOIN  `accidents_table` at ON vaj.`Collision_ID (PK)` = at.`Collision_ID (PK)`
WHERE  at.`Pre_Crash` = 'Changing Lanes';










