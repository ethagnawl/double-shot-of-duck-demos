--INSTALL quack FROM core_nightly;
--FORCE INSTALL quack;
FORCE INSTALL quack FROM core_nightly;
LOAD quack;

ATTACH 'quack:localhost' AS remote_db (TOKEN 'super_secret');

select * from remote_db.frames;

--insert into remote_db.frames (id, camera_id, captured_at, embedding, image_uri) values (
--    uuid(),
--    'foo-cam',
--    now(),
--    array(SELECT 0.0::FLOAT FROM range(512))::FLOAT[512],
--    'nice.jpg'
--);
