
        CREATE TABLE IF NOT EXISTS kinect_atlas_dev_stage.heartbeat_stats (
        concat_business_key   varchar (4000)
,arrival_ts   TIMESTAMP  NOT NULL
,heartbeat_id   int  NOT NULL
,message   varchar (4000)
,cdc_action   varchar (4000)

        ,PRIMARY KEY (heartbeat_id,arrival_ts)
        )
;