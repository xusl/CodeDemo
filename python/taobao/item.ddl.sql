/******************************************************************************/
/***                                 Tables                                 ***/
/******************************************************************************/


CREATE TABLE ITEM (
    NUM_IID            BIGINT,
    TITLE              VARCHAR(384) CHARACTER SET UTF8,
    NICK               VARCHAR(48) CHARACTER SET UTF8,
    ITEM_TYPE          SMALLINT,
    CID                BIGINT,
    SELLER_CIDS        VARCHAR(384) CHARACTER SET ASCII,
    LOCAL_CID		   BIGINT,	
    PROPS              VARCHAR(3072) CHARACTER SET ASCII,
    INPUT_PIDS         VARCHAR(4000) CHARACTER SET ASCII,
    INPUT_STR          VARCHAR(4000) CHARACTER SET UTF8,
    DESCRIPTION        BLOB SUB_TYPE 1 SEGMENT SIZE 1024 CHARACTER SET UTF8,
    NUM                INTEGER,
    VALID_THRU         SMALLINT,
    LIST_TIME          TIMESTAMP,
    DELIST_TIME        TIMESTAMP,
    STUFF_STATUS       SMALLINT,
    LOCATION_CITY      VARCHAR(48) CHARACTER SET UTF8,
    LOCATION_STATE     VARCHAR(32) CHARACTER SET UTF8,
    PRICE              NUMERIC(18,4),
    POST_FEE           NUMERIC(18,4),
    EXPRESS_FEE        NUMERIC(18,4),
    EMS_FEE            NUMERIC(18,4),
    HAS_DISCOUNT       SMALLINT,
    FREIGHT_PAYER      SMALLINT,
    HAS_INVOICE        SMALLINT,
    HAS_WARRANTY       SMALLINT,
    HAS_SHOWCASE       SMALLINT,
    CREATED            TIMESTAMP,
    MODIFIED           TIMESTAMP,
    AUCTION_INCREMENT  VARCHAR(32) CHARACTER SET ASCII,
    APPROVE_STATUS     SMALLINT,
    POSTAGE_ID         BIGINT,
    PRODUCT_ID         BIGINT,
    AUCTION_POINT      INTEGER,
    PROPERTY_ALIAS     VARCHAR(1024) CHARACTER SET UTF8,
    OUTER_ID           VARCHAR(96) CHARACTER SET UTF8,
    IS_VIRTUAL         SMALLINT,
    IS_TIMING          SMALLINT,
    VOLUME             BIGINT,
    AUTO_FILL			SMALLINT,
    SECOND_KILL        SMALLINT,
    PROPS_NAME         VARCHAR(2000) CHARACTER SET UTF8,
    BANNER			   SMALLINT,    
    VIOLATION          SMALLINT,
    AFTER_SALE_ID		BIGINT,
    SELL_PROMISE		SMALLINT,
    COD_POSTAGE_ID		BIGINT,    
    SATISFACTION_GUARANTEE  SMALLINT,
    SYNC_STATUS        SMALLINT,
    CLIENT_ID          VARCHAR(38) CHARACTER SET ASCII NOT NULL,
	CLIENT_IS_DELETE	SMALLINT DEFAULT 0,
	UPLOAD_FAIL_MSG		VARCHAR(1024) CHARACTER SET UTF8,	
	CLIENT_IS_SELECTED			SMALLINT,
	CLIENT_CUSTOM_GROUP_ID		BIGINT,
	CLIENT_NAVIGATION_TYPE		SMALLINT,
	IS_LIGHTNING_CONSIGNMENT SMALLINT,
	IS_XINPIN SMALLINT,
	CANEDIT_LIGHTNING_CONSIGNMENT SMALLINT,
	PARAMETERS          BLOB SUB_TYPE 1 SEGMENT SIZE 1024 CHARACTER SET UTF8,
	FEATURES			BLOB SUB_TYPE 1 SEGMENT SIZE 1024 CHARACTER SET UTF8,
	EMPTY_FIELDS         BLOB SUB_TYPE 1 SEGMENT SIZE 1024 CHARACTER SET UTF8,
	GLOBAL_STOCK_TYPE	SMALLINT,
	SUB_STOCK	SMALLINT,
	ITEM_WEIGHT VARCHAR(16) CHARACTER SET UTF8,
	ITEM_SIZE VARCHAR(16) CHARACTER SET UTF8
);




/******************************************************************************/
/***                           Unique Constraints                           ***/
/******************************************************************************/

ALTER TABLE ITEM ADD CONSTRAINT ITEM_UNIQUE_NUM_IID UNIQUE (NUM_IID);


/******************************************************************************/
/***                              Primary Keys                              ***/
/******************************************************************************/

ALTER TABLE ITEM ADD CONSTRAINT PK_ITEM PRIMARY KEY (CLIENT_ID);


CREATE INDEX IDX_ITEM_TYPE ON ITEM (CLIENT_NAVIGATION_TYPE, CLIENT_IS_DELETE, PRICE, CREATED);
CREATE INDEX IDX_ITEM_ISDELETE ON ITEM (CLIENT_IS_DELETE);
CREATE INDEX IDX_ITEM_LOCALCID ON ITEM (LOCAL_CID, CLIENT_NAVIGATION_TYPE);
/******************************************************************************/
/***                          Fields descriptions                           ***/
/******************************************************************************/

COMMENT ON COLUMN ITEM.TITLE IS 
'商品标题,不能超过60字节';

COMMENT ON COLUMN ITEM.NICK IS 
'卖家昵称';

COMMENT ON COLUMN ITEM.ITEM_TYPE IS 
'商品类型(fixed:一口价;auction:拍卖)注：取消团购';

COMMENT ON COLUMN ITEM.CID IS 
'商品所属的叶子类目 id';

COMMENT ON COLUMN ITEM.SELLER_CIDS IS 
'商品所属的店铺内卖家自定义类目列表';

COMMENT ON COLUMN ITEM.LOCAL_CID IS 
'商品所属的本地分类id';

COMMENT ON COLUMN ITEM.PROPS IS 
'商品属性 格式：pid:vid;pid:vid';

COMMENT ON COLUMN ITEM.INPUT_PIDS IS 
'用户自行输入的类目属性ID串。结构："pid1,pid2,pid3"，如："20000"（表示品牌） 注：通常一个类目下用户可输入的关键属性不超过1个。';

COMMENT ON COLUMN ITEM.INPUT_STR IS 
'用户自行输入的子属性名和属性值，结构:"父属性值;一级子属性名;一级子属性值;二级子属性名;自定义输入值,....",如：“耐克;耐克系列;科比系列;科比系列;2K5”，input_str需要与input_pids一一对应，注：通常一个类目下用户可输入的关键属性不超过1个。所有属性别名加起来不能超过 3999字节';

COMMENT ON COLUMN ITEM.NUM IS 
'商品数量';

COMMENT ON COLUMN ITEM.VALID_THRU IS 
'有效期,7或者14（默认是14天）';

COMMENT ON COLUMN ITEM.LIST_TIME IS 
'上架时间（格式：yyyy-MM-dd HH:mm:ss）';

COMMENT ON COLUMN ITEM.DELIST_TIME IS 
'下架时间（格式：yyyy-MM-dd HH:mm:ss）';

COMMENT ON COLUMN ITEM.STUFF_STATUS IS 
'商品新旧程度(全新:new，闲置:unused，二手：second)';

COMMENT ON COLUMN ITEM.LOCATION_CITY IS 
'所在城市（中文名称）';

COMMENT ON COLUMN ITEM.LOCATION_STATE IS 
'所在省份（中文名称）';

COMMENT ON COLUMN ITEM.PRICE IS 
'商品价格，格式：5.00；单位：元；精确到：分';

COMMENT ON COLUMN ITEM.POST_FEE IS 
'平邮费用,格式：5.00；单位：元；精确到：分';

COMMENT ON COLUMN ITEM.EXPRESS_FEE IS 
'快递费用,格式：5.00；单位：元；精确到：分';

COMMENT ON COLUMN ITEM.EMS_FEE IS 
'ems费用,格式：5.00；单位：元；精确到：分';

COMMENT ON COLUMN ITEM.HAS_DISCOUNT IS 
'支持会员打折,true/false';

COMMENT ON COLUMN ITEM.FREIGHT_PAYER IS 
'运费承担方式,seller（卖家承担），buyer(买家承担）';

COMMENT ON COLUMN ITEM.HAS_INVOICE IS 
'是否有发票,TRUE/FALSE';

COMMENT ON COLUMN ITEM.HAS_WARRANTY IS 
'是否有保修,true/false';

COMMENT ON COLUMN ITEM.HAS_SHOWCASE IS 
'橱窗推荐,true/false';

COMMENT ON COLUMN ITEM.MODIFIED IS 
'商品修改时间（格式：yyyy-MM-dd HH:mm:ss）';

COMMENT ON COLUMN ITEM.AUCTION_INCREMENT IS 
'加价幅度。如果为0，代表系统代理幅度。在竞拍中，为了超越上一个出价，会员需要在当前出价上增加金额，这个金额就是加价幅度。卖家在发布宝贝的时候可以自定义加价幅度，也可以让系统自动代理加价。系统自动代理加价的加价幅度随着当前出价金额的增加而增加，我们建议会员使用系统自动代理加价，并请买家在出价前看清楚加价幅度的具体金额。另外需要注意是，此功能只适用于拍卖的商品。以下是系统自动代理加价幅度表：当前价（加价幅度 ） 1-40（ 1 ）、41-100（ 2 ）、101-200（5 ）、201-500 （10）、501-1001（15）、001-2000（25）、2001-5000（50）、5001-10000（100） 10001以上 200';


COMMENT ON COLUMN ITEM.APPROVE_STATUS IS 
'商品上传后的状态。onsale出售中，instock库中';

COMMENT ON COLUMN ITEM.POSTAGE_ID IS 
'宝贝所属的运费模板ID，如果没有返回则说明没有使用运费模板';

COMMENT ON COLUMN ITEM.PRODUCT_ID IS 
'宝贝所属产品的id(可能为空). 该字段可以通过taobao.products.search 得到';

COMMENT ON COLUMN ITEM.AUCTION_POINT IS 
'返点比例';

COMMENT ON COLUMN ITEM.PROPERTY_ALIAS IS 
'属性值别名';

COMMENT ON COLUMN ITEM.OUTER_ID IS 
'商家外部编码(可与商家外部系统对接)';

COMMENT ON COLUMN ITEM.IS_VIRTUAL IS 
'虚拟商品的状态字段';

COMMENT ON COLUMN ITEM.IS_TIMING IS 
'是否定时上架商品';

COMMENT ON COLUMN ITEM.SECOND_KILL IS 
'秒杀商品类型。打上秒杀标记的商品，用户只能下架并不能再上架，其他任何编辑或删除操作都不能进行。如果用户想取消秒杀标记，需要联系小二进行操作。如果秒杀结束需要自由编辑请联系活动负责人（小二）去掉秒杀标记。可选类型 web_only(只能通过web网络秒杀) wap_only(只能通过wap网络秒杀) web_and_wap(既能通过web秒杀也能通过wap秒杀)';

COMMENT ON COLUMN ITEM.PROPS_NAME IS 
'商品属性名称。标识着props内容里面的pid和vid所对应的名称。格式为：pid1:vid1:pid_name1:vid_name1;pid2:vid2:pid_name2:vid_name2……';

COMMENT ON COLUMN ITEM.AFTER_SALE_ID IS 
'售后服务ID';

COMMENT ON COLUMN ITEM.SATISFACTION_GUARANTEE IS 
'卖家退换货承诺：卖家提供承诺true，卖家无承诺false';

COMMENT ON COLUMN ITEM.SYNC_STATUS IS 
'synchronization status 0x0000 unknown 0x';

COMMENT ON COLUMN ITEM.CLIENT_IS_DELETE IS
'商品是否已经被删除' ;

COMMENT ON COLUMN ITEM.UPLOAD_FAIL_MSG IS
'上传失败信息' ;

COMMENT ON COLUMN ITEM.BANNER IS
'出售中商品使用，出售中商品的状态' ;

COMMENT ON COLUMN ITEM.CLIENT_IS_SELECTED IS
'本地商品是否被选中' ;

COMMENT ON COLUMN ITEM.CLIENT_CUSTOM_GROUP_ID IS
'本地仓库中的宝贝和宝贝模板专用，商品所在的用户自定义分组id' ;

COMMENT ON COLUMN ITEM.CLIENT_NAVIGATION_TYPE IS
'宝贝所在的大分类 0x00 未知分组，0x01 本地库存，0x02表示出售中宝贝，0x03表示线上仓库中的宝贝，0x04搜索结果，0x05回收站，0x06宝贝模板' ;

COMMENT ON COLUMN ITEM.GLOBAL_STOCK_TYPE IS
'全球购类型' ;

COMMENT ON COLUMN ITEM.SUB_STOCK IS
'库存计数' ;

/******************************************************************************/
/***                                 Tables                                 ***/
/******************************************************************************/



CREATE TABLE PICTURE (
    ID             BIGINT,
    URL            VARCHAR(2048) CHARACTER SET UTF8,
    PROPERTIES     VARCHAR(256) CHARACTER SET ASCII,
    POS     SMALLINT DEFAULT 0,
    CREATED        TIMESTAMP,
    NUM_IID			BIGINT,
    CLIENT_ID      VARCHAR(38) NOT NULL,
    CLIENT_ITEMID  VARCHAR(38) CHARACTER SET ASCII,
    CLIENT_TYPE    SMALLINT,
    CLIENT_STATUS  SMALLINT,
    CLIENT_NAME    VARCHAR(64) CHARACTER SET ASCII
);

CREATE INDEX IDX_PICTURE_ITEMID_TYPE_POS ON PICTURE (CLIENT_ITEMID, CLIENT_TYPE, POS);


/******************************************************************************/
/***                              Primary Keys                              ***/
/******************************************************************************/

ALTER TABLE PICTURE ADD CONSTRAINT PK_PICTURE PRIMARY KEY (CLIENT_ID);


/******************************************************************************/
/***                          Fields descriptions                           ***/
/******************************************************************************/

COMMENT ON COLUMN PICTURE.ID IS 
'商品图片的id，和商品相对应';

COMMENT ON COLUMN PICTURE.URL IS 
'图片链接地址';

COMMENT ON COLUMN PICTURE.PROPERTIES IS 
'图片所对应的属性组合的字符串';

COMMENT ON COLUMN PICTURE.POS IS 
'图片放在第几张（多图时可设置）';

COMMENT ON COLUMN PICTURE.CREATED IS 
'图片创建时间 时间格式：yyyy-MM-dd HH:mm:ss';

COMMENT ON COLUMN PICTURE.CLIENT_NAME IS 
'宝贝图片的MD5值';

COMMENT ON COLUMN PICTURE.CLIENT_ID IS 
'图片本地id';

COMMENT ON COLUMN PICTURE.CLIENT_ITEMID IS 
'商品本地id';

COMMENT ON COLUMN PICTURE.CLIENT_TYPE IS 
'宝图片类型 1：商品多图 2：属性关联图片(sku图片)';

COMMENT ON COLUMN PICTURE.CLIENT_STATUS IS 
'1：正常，2:更改，-1：删除';


/******************************************************************************/
/***                                 Tables                                 ***/
/******************************************************************************/



CREATE TABLE SKU (
    SKU_ID         BIGINT,
    NUM_IID        BIGINT,
    PROPERTIES     VARCHAR(1024) CHARACTER SET ASCII,
    QUANTITY       BIGINT,
    PRICE          NUMERIC(18,4),
    OUTER_ID       VARCHAR(128) CHARACTER SET UTF8,
    CREATED			TIMESTAMP,
    MODIFIED		TIMESTAMP,
    STATUS			VARCHAR(32) CHARACTER SET ASCII,
    CLIENT_ID      VARCHAR(38) CHARACTER SET ASCII NOT NULL,
    CLIENT_STATUS  SMALLINT,
    CLIENT_ITEMID  VARCHAR(38) CHARACTER SET ASCII,
    PROPERTIES_NAME VARCHAR(1024) CHARACTER SET UTF8
);




/******************************************************************************/
/***                              Primary Keys                              ***/
/******************************************************************************/

ALTER TABLE SKU ADD CONSTRAINT PK_SKU PRIMARY KEY (CLIENT_ID);

CREATE INDEX IDX_SKU_ITEMID ON SKU (CLIENT_ITEMID);
/******************************************************************************/
/***                          Fields descriptions                           ***/
/******************************************************************************/

COMMENT ON COLUMN SKU.NUM_IID IS 
'宝贝数字id';

COMMENT ON COLUMN SKU.PROPERTIES IS 
'sku的销售属性组合字符串（颜色，大小，等等，可通过类目API获取某类目下的销售属性）,格式是p1:v1;p2:v2';

COMMENT ON COLUMN SKU.QUANTITY IS 
'属于这个sku的商品的数量';

COMMENT ON COLUMN SKU.PRICE IS 
'属于这个sku的商品的价格 取值范围:0-100000000;精确到2位小数;单位:元。如:200.07，表示:200元7分。';

COMMENT ON COLUMN SKU.OUTER_ID IS 
'商家设置的外部id';

COMMENT ON COLUMN SKU.CLIENT_ID IS 
'SKU的本地ID';
COMMENT ON COLUMN SKU.CLIENT_STATUS IS 
'SKU的状态 1 正常，-1删除，2更改';
COMMENT ON COLUMN SKU.CLIENT_ITEMID IS 
'SKU对应商品的本地ID';
COMMENT ON COLUMN SKU.PROPERTIES_NAME IS 
'自定义销售属性的名字';

/******************************************************************************/
/***                                 Tables                                 ***/
/******************************************************************************/



CREATE TABLE VIDEO (
    ID             BIGINT,
    VIDEO_ID       BIGINT,
    NUM_IID        BIGINT,
    URL            VARCHAR(512) CHARACTER SET UTF8,
    CREATED        TIMESTAMP,
    MODIFIED       TIMESTAMP,
    PREVIEWURL		VARCHAR(1024) CHARACTER SET UTF8,
    CLIENT_ID      VARCHAR(38) CHARACTER SET ASCII NOT NULL,
    CLIENT_ITEMID  VARCHAR(38) CHARACTER SET ASCII,
    CLIENT_STATUS  SMALLINT
);




/******************************************************************************/
/***                              Primary Keys                              ***/
/******************************************************************************/

ALTER TABLE VIDEO ADD CONSTRAINT PK_VIDEO PRIMARY KEY (CLIENT_ID);


/******************************************************************************/
/***                          Fields descriptions                           ***/
/******************************************************************************/

COMMENT ON COLUMN VIDEO.ID IS 
'视频关联记录的id，和商品相对应
';

COMMENT ON COLUMN VIDEO.VIDEO_ID IS 
'视频关联记录的id，和商品相对应';

COMMENT ON COLUMN VIDEO.NUM_IID IS 
'视频记录所关联的商品的数字id';

COMMENT ON COLUMN VIDEO.URL IS 
'video的url连接地址。淘秀里视频记录里面存储的url地址';

COMMENT ON COLUMN VIDEO.CREATED IS 
'视频关联记录创建时间（格式：yyyy-MM-dd HH:mm:ss）';

COMMENT ON COLUMN VIDEO.MODIFIED IS 
'视频关联记录修改时间（格式：yyyy-MM-dd HH:mm:ss）';

COMMENT ON COLUMN VIDEO.CLIENT_ID IS 
'视频的本地ID';

COMMENT ON COLUMN VIDEO.CLIENT_ITEMID IS 
'视频关联的商品的本地ID';

COMMENT ON COLUMN VIDEO.CLIENT_STATUS IS 
'视频的状态 1:正常，-1：删除';

/******************************************************************************/
/***                                 Tables                                 ***/
/******************************************************************************/



CREATE TABLE AFTERSALE (
    AFTER_SALE_ID    BIGINT,
    AFTER_SALE_NAME  VARCHAR(40) CHARACTER SET UTF8
);

/******************************************************************************/
/***                          Fields descriptions                           ***/
/******************************************************************************/

COMMENT ON COLUMN AFTERSALE.AFTER_SALE_ID IS 
'售后说明模板的线上ID';

COMMENT ON COLUMN AFTERSALE.AFTER_SALE_NAME IS 
'售后说明模板的名称';
