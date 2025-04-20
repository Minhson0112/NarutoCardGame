INSERT INTO `weapon_templates`
  (
    `weapon_key`,
    `name`,
    `grade`,
    `bonus_health`,
    `bonus_armor`,
    `bonus_damage`,
    `bonus_crit_rate`,
    `bonus_speed`,
    `bonus_chakra`,
    `image_url`,
    `sell_price`
  )
VALUES
  ('Kunai',       'Kunai',       'Normal',  NULL,    NULL, 50,  0.02, NULL, NULL, 'Kunai150',      500000),
  ('Knife',       'Knife',       'Normal', 200,     NULL,   NULL, NULL, 0.03, NULL, 'Knife160',      500000),
  ('ChakraKnife', 'ChakraKnife', 'Normal',  NULL,    8,    NULL, NULL, NULL, 20,  'ChakraKnife170',500000),
  ('Guandao',     'Guandao',     'Normal',  NULL,    NULL,   60,  NULL, NULL, 20,  'Guandao180',    500000),
  ('Katana',      'Katana',      'Normal', 250,     NULL,   58,  NULL, NULL, NULL, 'Katana190',     500000),
  ('Shuriken',    'Shuriken',    'Normal',  NULL,    6,    NULL, NULL, 0.03, NULL, 'Shuriken200',   500000),
  ('Bow',         'Bow',         'Normal',  NULL,    NULL,   NULL, NULL, 0.03, 20,  'Bow210',        500000),
  ('Flail',       'Flail',       'Normal', 220,     NULL,   NULL, 0.02, NULL, NULL, 'Flail220',      500000),
  ('Kibaku',      'Kibaku',      'Normal',  NULL,    10,    42,   NULL, NULL, NULL, 'Kibaku230',     500000),
  ('Tansa',       'Tansa',       'Normal',  NULL,    NULL,   NULL, 0.02, NULL, 20,  'Tansa250',      500000),

  ('Tessen',   'Tessen',   'Rare',  430, 10, 70,  NULL, 0.06, NULL, 'Tessen430',   1500000),
  ('Sansaju',  'Sansaju',  'Rare',  440, NULL, 75, 0.04, 0.06, 40,  'Sansaju440',  1500000),
  ('Suna',     'Suna',     'Rare',  NULL, 8, 64,  NULL, 0.06, 40,  'Suna450',     1500000),
  ('Enma',     'Enma',     'Rare',  480, 12, NULL, 0.04, 0.06, NULL, 'Enma480',     1500000),
  ('Samehada', 'Samehada', 'Rare',  500, NULL, 85, 0.04, NULL, 40,  'Samehada500', 1500000),

  ('Rinnegan', 'Rinnegan', 'Legendary', 600, 13, 120, 0.05, 0.09, 60, 'Rinnegan600',  4000000),
  ('Gudodama', 'Gudodama', 'Legendary', 700, 16, 100, 0.05, 0.09, 60, 'Gudodama700',  4000000);
