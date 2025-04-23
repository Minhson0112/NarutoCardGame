-- 1. Xoá toàn bộ dữ liệu cũ
DELETE FROM `card_templates`;

-- 2. Nhập lại toàn bộ thẻ với cấu trúc mới
INSERT INTO `card_templates`
  (card_key, name, tier, element, image_url, sell_price,
   health, armor, base_damage, crit_rate, speed, chakra, first_position)
VALUES

  ('Yamanaka_Ino',    'Yamanaka Ino',       'Genin',    'Thủy', 'ino',      3000, 765,  10, 24, 0.03, 0.02, 40, FALSE),
  ('TenTen',          'TenTen',              'Genin',    'Phong','tenten',   3000, 770,  7, 31, 0.04, 0.05, 20, FALSE),
  ('Kankuro',         'Kankuro',             'Genin',    'Hỏa',  'kankuro',  3000, 742,  11, 42, 0.07, 0.04, 60, FALSE),
  ('Aburame_Shino',   'Aburame Shino',       'Genin',    'Phong','shino',    3000, 802,  6, 40, 0.06, 0.03, 20, FALSE),
  ('Haruno_Sakura',   'Haruno Sakura',       'Genin',    'Thủy','sakura',    3000, 821,  10, 26, 0.08, 0.08, 20, FALSE),
  ('Hyuga_Hinata',    'Hyuga Hinata',        'Genin',    'Thể',  'hinata',   3000, 1069,  15, 20, 0.05, 0.1, 0, TRUE),
  ('Temari',          'Temari',              'Genin',    'Phong','temari',   3000, 689,  8, 44, 0.10, 0.05, 40, FALSE),
  ('Inuzuka_Kiba',    'Inuzuka Kiba',        'Genin',    'Thổ',  'kiba',     3000, 836,  9, 32, 0.03, 0.05, 20, FALSE),
  ('Akimichi_Choji',  'Akimichi Choji',      'Genin',    'Thổ',  'choji',    3000, 1245,  12, 18, 0.03, 0.07, 20, TRUE),
  ('Umino_Iruka',     'Umino Iruka',         'Genin',    'Hỏa',  'iruka',    3000, 912,  6, 38, 0.1, 0.02, 0, FALSE),
  ('Momochi_Zabuza',  'Momochi Zabuza',      'Genin',    'Thủy','zabuza',    3000, 1121,  17, 27, 0.03, 0.05, 40, TRUE),
  ('Konohamaru',      'Konohamaru',          'Genin',    'Hỏa',  'konohamaru',3000, 758,  6, 41, 0.08, 0.06, 0, FALSE),

  ('Hyuga_Neji', 'Hyuga Neji', 'Chunin', 'Thể', 'neji', 20000, 1339, 18, 43, 0.09, 0.06, 20, TRUE),
  ('Nara_Shikamaru', 'Nara Shikamaru', 'Chunin', 'Thổ', 'shikamaru', 20000, 1074, 12, 58, 0.07, 0.05, 20, FALSE),
  ('Nohara_Rin', 'Nohara Rin', 'Chunin', 'Thủy', 'rin', 20000, 1024, 12, 51, 0.08, 0.03, 60, FALSE),
  ('Yagura', 'Yagura', 'Chunin', 'Thủy', 'yagura', 20000, 1354, 17, 46, 0.08, 0.06, 40, TRUE),
  ('Rock_Lee', 'Rock Lee', 'Chunin', 'Thể', 'lee', 20000, 1043, 12, 56, 0.07, 0.08, 60, FALSE),
  ('Yuhi_Kurenai', 'Yuhi Kurenai', 'Chunin', 'Phong', 'kurenai', 20000, 1066, 14, 52, 0.15, 0.10, 20, FALSE),
  ('Sarutobi_Asuma', 'Sarutobi Asuma', 'Chunin', 'Phong', 'asuma', 20000, 1013, 13, 53, 0.20, 0.05, 60, FALSE),
  ('Hidan', 'Hidan', 'Chunin', 'Thổ', 'hidan', 20000, 1375, 20, 40, 0.02, 0.15, 60, TRUE),
  ('Kimimaro', 'Kimimaro', 'Chunin', 'Thổ', 'kimimaro', 20000, 1334, 18, 41, 0.07, 0.04, 40, TRUE),
  ('Sasori', 'Sasori', 'Chunin', 'Phong', 'sasori', 20000, 1032, 13, 59, 0.25, 0.09, 20, FALSE),
  ('Yamanaka_Sai', 'Yamanaka Sai', 'Chunin', 'Hỏa', 'sai', 20000, 1098, 13, 55, 0.27, 0.06, 0, FALSE),
  ('Yakushi_Kabuto', 'Yakushi Kabuto', 'Chunin', 'Thổ', 'kabuto', 20000, 1025, 13, 56, 0.18, 0.07, 0, FALSE),
  ('Yamato', 'Yamato', 'Chunin', 'Thủy', 'yamato', 20000, 1051, 13, 57, 0.10, 0.03, 60, FALSE),
  ('Deidara', 'Deidara', 'Chunin', 'Thổ', 'deidara', 20000, 1094, 12, 60, 0.20, 0.10, 20, FALSE),
  ('Gaara', 'Gaara', 'Chunin', 'Thổ', 'gaara', 20000, 1072, 14, 62, 0.19, 0.07, 0, FALSE),
  ('Chunin_Kakashi', 'Chunin Kakashi', 'Chunin', 'Lôi', 'chuninkakashi', 20000, 1035, 12, 65, 0.25, 0.08, 20, FALSE),
  ('Kakuzu', 'Kakuzu', 'Chunin', 'Thổ', 'kakuzu', 20000, 1326, 17, 47, 0.06, 0.03, 0, TRUE),
  ('Kushina', 'Kushina', 'Chunin', 'Phong', 'kushina', 20000, 1061, 14, 68, 0.15, 0.06, 40, FALSE),

  ('Konan', 'Konan', 'Jounin', 'Hỏa', 'konan', 80000, 1419, 15, 81, 0.19, 0.10, 40, FALSE),
  ('Kisame', 'Kisame', 'Jounin', 'Thủy', 'kisame', 80000, 1878, 21, 72, 0.25, 0.10, 60, TRUE),
  ('Uchiha_Obito', 'Uchiha Obito', 'Jounin', 'Hỏa', 'obito', 80000, 1475, 14, 80, 0.28, 0.10, 20, FALSE),
  ('Gengetsu', 'Gengetsu', 'Jounin', 'Thủy', 'gengetsu', 80000, 1316, 14, 94, 0.15, 0.10, 60, FALSE),
  ('Killer_Bee', 'Killer Bee', 'Jounin', 'Phong', 'bee', 80000, 1777, 22, 78, 0.20, 0.08, 20, TRUE),
  ('RaikageIII', 'RaikageIII', 'Jounin', 'Lôi', 'raikage', 80000, 1629, 21, 82, 0.19, 0.09, 0, TRUE),
  ('Uchiha_Itachi', 'Uchiha Itachi', 'Jounin', 'Hỏa', 'itachi', 80000, 1247, 16, 93, 0.27, 0.10, 0, FALSE),
  ('Pain', 'Pain', 'Jounin', 'Phong', 'pain', 80000, 1234, 14, 96, 0.23, 0.09, 20, FALSE),
  ('Uchiha_Sasuke', 'Uchiha Sasuke', 'Jounin', 'Hỏa', 'sasuke', 80000, 1253, 13, 101, 0.26, 0.09, 20, FALSE),
  ('Kyuubi_Naruto', 'Kyuubi Naruto', 'Jounin', 'Phong', '9naruto', 80000, 1308, 11, 104, 0.29, 0.10, 40, FALSE),


  ('Hokage_Kakashi', 'Hokage Kakashi', 'Kage', 'Thổ', 'hiruzen', 200000, 2437, 24, 116, 0.26, 0.10, 60, TRUE),
  ('Might_Guy', 'Might Guy', 'Kage', 'Thể', 'guy', 200000, 2502, 22, 119, 0.22, 0.12, 0, TRUE),
  ('Uzumaki_Nagato', 'Uzumaki Nagato', 'Kage', 'Thủy', 'nagato', 200000, 2101, 18, 127, 0.30, 0.09, 40, FALSE),
  ('Onoki', 'Onoki', 'Kage', 'Thổ', 'onoki', 200000, 2297, 17, 123, 0.28, 0.09, 20, FALSE),
  ('Terumi_Mei', 'Terumi Mei', 'Kage', 'Thủy', 'mei', 200000, 2024, 16, 122, 0.30, 0.09, 20, FALSE),
  ('Tsunade', 'Tsunade', 'Kage', 'Thủy', 'tsunade', 200000, 2169, 18, 121, 0.24, 0.08, 60, FALSE),
  ('Orochimaru', 'Orochimaru', 'Kage', 'Thổ', 'orochimaru', 200000, 2574, 25, 97, 0.22, 0.08, 40, TRUE),
  ('Jiraiya', 'Jiraiya', 'Kage', 'Hỏa', 'jiraiya', 200000, 2200, 15, 128, 0.29, 0.09, 60, FALSE),
  ('Minato', 'Minato', 'Kage', 'Lôi', 'minato', 200000, 2117, 15, 132, 0.30, 0.10, 20, FALSE),
  ('Sarutobi_Hiruzen', 'Sarutobi Hiruzen', 'Kage', 'Hỏa', 'hiruzen', 200000, 2212, 16, 125, 0.27, 0.09, 20, FALSE),
  ('Senju_Tobirama', 'Senju Tobirama', 'Kage', 'Thể', 'tobirama', 200000, 2700, 22, 93, 0.23, 0.10, 0, TRUE),
  ('Uchiha_Madara', 'Uchiha Madara', 'Kage', 'Hỏa', 'madara', 200000, 2174, 14, 129, 0.28, 0.10, 0, FALSE),
  ('Senju_Hashirama', 'Senju Hashirama', 'Kage', 'Hỏa', 'hashirama', 200000, 2249, 13, 121, 0.25, 0.10, 0, FALSE),

  ('Shimura_Danzo', 'Shimura Danzo', 'Legendary', 'Hỏa', 'danzo', 500000, 2924, 21, 138, 0.27, 0.09, 0, FALSE),
  ('Haku', 'Haku', 'Legendary', 'Thủy', 'haku', 500000, 3224, 32, 112, 0.24, 0.08, 40, TRUE),
  ('Hatake_Kakashi', 'Hatake Kakashi', 'Legendary', 'Lôi', 'kakashi', 500000, 3021, 21, 134, 0.28, 0.10, 60, FALSE),
  ('Uzumaki_Naruto', 'Uzumaki Naruto', 'Legendary', 'Phong', 'naruto', 500000, 3087, 22, 142, 0.29, 0.09, 40, FALSE),
  ('Susanoo_Sasuke', 'Susanoo Sasuke', 'Legendary', 'Hỏa', 'susanoosasuke', 500000, 2802, 21, 140, 0.30, 0.10, 0, FALSE),
  ('Six_Paths_Pain', 'Six Paths Pain', 'Legendary', 'Phong', '6pain', 500000, 2798, 23, 145, 0.26, 0.10, 20, FALSE),
  ('Akatsuki_Itachi', 'Akatsuki Itachi', 'Legendary', 'Hỏa', 'akatsukiitachi', 500000, 2963, 20, 153, 0.30, 0.10, 20, FALSE);


ALTER TABLE `card_templates`
MODIFY COLUMN `tier` VARCHAR(20) NOT NULL;
