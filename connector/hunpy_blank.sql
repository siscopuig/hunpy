-- MySQL dump 10.13  Distrib 5.7.23, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: hunpy
-- ------------------------------------------------------
-- Server version	5.7.23-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `AdServer`
--

DROP TABLE IF EXISTS `AdServer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `AdServer` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `domain` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=115 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `AdServer`
--

LOCK TABLES `AdServer` WRITE;
/*!40000 ALTER TABLE `AdServer` DISABLE KEYS */;
INSERT INTO `AdServer` (`id`, `domain`) VALUES (1,'cdn.oas-eu1.adnxs.com'),(2,'ad.doubleclick.net'),(3,'secure.flashtalking.com'),(4,'s0.2mdn.net'),(5,'ds.serving-sys.com'),(6,'s1.2mdn.net'),(7,'tpc.googlesyndication.com'),(8,'pagead2.googlesyndication.com'),(9,'assets.rubiconproject.com'),(10,'cdn.atlassbx.com'),(11,'img.cdns.turn.com'),(12,'speed.pointroll'),(13,'cdn.w55c.net'),(14,'www.wsoddata.com'),(15,'ab167334.adbutler-exciton.com'),(16,'s1.adform.net'),(17,'cdn.ctnsnet.com'),(18,'img.mediaplex.com'),(19,'cmc-marke-cmc-markets.bannerflow.com'),(20,'cstatic.weborama.fr'),(21,'s3-eu-west-1.amazonaws.com'),(22,'www.dianomi.com'),(23,'oasc-eu1.247realmedia.com'),(24,'bbgox.bbg-online.de'),(25,'datasource.fondsprofessionell.com'),(26,'aka-cdn-ns.adtech.de'),(27,'aka-cdn.adtech.de'),(28,'ad1.emediate.dk'),(29,'cdn.flashtalking.com'),(30,'secure-nym.adnxs.com'),(31,'ej-ad.s3.amazonaws.com'),(32,'imagesrv.adition.com'),(33,'secure-assets.rubiconproject.com'),(34,'secure.flashtalking.com'),(35,'ads.w55c.net'),(36,'ams1-ib.adnxs.com'),(37,'fra1-ib.adnxs.com'),(38,'fw.adsafeprotected.com'),(39,'cdn.adnxs.com'),(40,'cdn.adsfactor.net'),(41,'secure-ds.serving-sys.com'),(42,'pool.admedo.com'),(43,'img.adplan-ds.com '),(44,'content.aimatch.com'),(45,'img.ak.impact-ad.jp'),(46,'pubads.g.doubleclick.net'),(47,'vcdn.adnxs.com'),(48,'datasource.fa-mag.com'),(49,'cdn.oas-c18.adnxs.com'),(50,'ab167548.adbutler-ikon.com'),(51,'images2.ads.rcsobjects.it'),(52,'datasource.fa-mag.com'),(53,'fi.intms.nl'),(54,'ad.bluerating.com'),(55,'ced.sascdn.com '),(56,'efund.media'),(57,'banners.host.bannerflow.com'),(58,'gfx.finanztreff.de'),(59,'unibet-unibet.bannerflow.com'),(60,'static.snapmobile.asia'),(61,'s1.adformdsp.net'),(62,'html5.adsrvr.org'),(63,'a.rfihub.com'),(64,'server-m.vocento.com'),(65,'s.atemda.com'),(66,'d13.zedo.com'),(67,'cashonline.serverhoster.de'),(68,'ad13.adfarm1.adition.com'),(69,'static.nrc.nl'),(70,'vcdn.adnxs.com'),(71,'media.adrcdn.com'),(72,'d13.zedo.com'),(73,'np-adimage.newscloud.or.kr'),(74,'adimg.imbc.com'),(75,'ad.kmib.co.kr'),(76,'img.realdsp.co.kr'),(77,'openx2.mediamatis.com'),(78,'ad.adsrvr.org'),(79,'servedbyadbutler.com'),(80,'ad.wsodcdn.com'),(81,'assets.incisivemedia.com'),(82,'ad.atdmt.com'),(83,'d31i2625d5nv27.cloudfront.net'),(84,'cdn.oas-c17.adnxs.com'),(85,'s.adroll.com'),(86,'ubmcmm.baidustatic.com'),(87,'falcon-creative-cloudcdn.pixfs.net'),(88,'tveta.naver.net'),(89,'img.funddoctor.co.kr'),(90,'ads.emetro.co.kr'),(91,'img.realdsp.co.kr'),(92,'hcimg.realclick.co.kr'),(93,'s3.eu-central-1.amazonaws.com'),(94,'streaming.ad-balancer.at'),(95,'a248.e.akamai.net'),(96,'ad.charltonmedia.com'),(97,'cdn.asn.advolution.de'),(98,'du3rcmbgk4e8q.cloudfront.net'),(99,'ds-cc.serving-sys.com'),(100,'images.informatm.com'),(101,'g1.dfcfw.com'),(102,'adpic.chinadaily.com.cn'),(103,'afp.alicdn.com'),(104,'c1.ifengimg.com'),(105,'peoplecitic.com'),(106,'info.stockstar.com'),(107,'itv.hexun.com'),(108,'img.cnfol.com'),(109,'static-alias-1.360buyimg.com'),(110,'showimg.caixin.com'),(111,'img.tbnimg.com'),(112,'ipengtai.huanqiu.com'),(113,'wmcdn.qtmojo.cn'),(114,'r.takungpao.com');
/*!40000 ALTER TABLE `AdServer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Adverts`
--

DROP TABLE IF EXISTS `Adverts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Adverts` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `ad_uid` varchar(64) DEFAULT NULL,
  `datetime` datetime DEFAULT NULL,
  `domain` varchar(255) DEFAULT NULL,
  `src` varchar(512) DEFAULT NULL,
  `width` smallint(11) unsigned DEFAULT NULL,
  `height` smallint(11) unsigned DEFAULT NULL,
  `x` smallint(6) unsigned DEFAULT NULL,
  `y` smallint(6) unsigned DEFAULT NULL,
  `processed` tinyint(1) DEFAULT '0',
  `landing` varchar(512) DEFAULT NULL,
  `finfo` varchar(40) DEFAULT NULL,
  `server` varchar(64) DEFAULT NULL,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_modified` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `ad_uid` (`ad_uid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Adverts`
--

LOCK TABLES `Adverts` WRITE;
/*!40000 ALTER TABLE `Adverts` DISABLE KEYS */;
/*!40000 ALTER TABLE `Adverts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `AdvertsStorage`
--

DROP TABLE IF EXISTS `AdvertsStorage`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `AdvertsStorage` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `is_ignore` tinyint(4) NOT NULL DEFAULT '0',
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `collected` tinyint(4) NOT NULL DEFAULT '0',
  `uid_dir` varchar(64) DEFAULT NULL,
  `ext` varchar(64) DEFAULT NULL,
  `filename` varchar(255) DEFAULT NULL,
  `fullpath` varchar(255) DEFAULT NULL,
  `last_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `uid_dir` (`uid_dir`),
  KEY `collected` (`collected`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `AdvertsStorage`
--

LOCK TABLES `AdvertsStorage` WRITE;
/*!40000 ALTER TABLE `AdvertsStorage` DISABLE KEYS */;
/*!40000 ALTER TABLE `AdvertsStorage` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Cycles`
--

DROP TABLE IF EXISTS `Cycles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Cycles` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `u_id` smallint(11) unsigned DEFAULT NULL,
  `cycles` smallint(11) unsigned DEFAULT '0',
  `date` date DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `last_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Cycles`
--

LOCK TABLES `Cycles` WRITE;
/*!40000 ALTER TABLE `Cycles` DISABLE KEYS */;
/*!40000 ALTER TABLE `Cycles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Instances`
--

DROP TABLE IF EXISTS `Instances`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Instances` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `ad_uid` varchar(64) DEFAULT NULL,
  `u_id` smallint(11) unsigned DEFAULT NULL,
  `counter` smallint(11) unsigned DEFAULT NULL,
  `date` date DEFAULT NULL,
  `last_modified` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Instances`
--

LOCK TABLES `Instances` WRITE;
/*!40000 ALTER TABLE `Instances` DISABLE KEYS */;
/*!40000 ALTER TABLE `Instances` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Placements`
--

DROP TABLE IF EXISTS `Placements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Placements` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `width` int(11) DEFAULT NULL,
  `height` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=163 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Placements`
--

LOCK TABLES `Placements` WRITE;
/*!40000 ALTER TABLE `Placements` DISABLE KEYS */;
INSERT INTO `Placements` (`id`, `width`, `height`) VALUES (1,970,250),(2,300,600),(3,300,250),(4,728,90),(5,160,600),(6,468,60),(7,120,600),(8,300,100),(9,780,450),(10,1000,100),(11,970,90),(12,990,100),(13,653,90),(14,660,87),(15,560,72),(16,250,250),(17,500,500),(18,600,500),(19,600,75),(20,980,240),(21,1070,90),(22,1500,900),(23,900,250),(24,980,90),(25,300,1050),(26,125,125),(27,940,250),(28,234,60),(29,120,240),(30,336,280),(31,320,50),(32,320,100),(33,120,60),(34,300,800),(35,940,60),(36,950,60),(37,1280,2000),(38,336,600),(39,970,220),(40,1000,180),(41,1000,200),(42,1000,250),(43,1000,300),(44,1000,540),(45,1280,900),(46,130,30),(47,130,200),(48,130,900),(49,1300,700),(50,1300,1024),(51,300,60),(52,300,80),(53,300,90),(54,300,300),(55,300,350),(56,300,500),(57,336,100),(58,336,850),(59,250,100),(60,250,300),(61,250,600),(62,728,100),(63,970,66),(64,970,160),(65,970,350),(66,970,600),(67,200,800),(68,200,600),(69,994,118),(70,994,250),(71,400,400),(72,500,1000),(73,1000,90),(74,250,640),(75,760,250),(76,960,250),(77,980,250),(78,1200,200),(79,770,250),(80,778,90),(81,960,90),(82,300,40),(83,150,30),(84,800,250),(85,980,100),(86,769,90),(87,515,180),(88,730,92),(89,432,60),(90,1002,160),(91,1000,160),(92,200,200),(93,990,90),(94,290,520),(95,290,260),(96,290,194),(97,475,90),(98,200,132),(99,150,300),(100,1150,90),(101,140,140),(102,140,60),(103,950,160),(104,1110,80),(105,420,500),(106,550,400),(107,700,100),(108,500,900),(109,770,90),(110,893,80),(111,670,85),(112,671,85),(113,145,85),(114,146,86),(115,735,85),(116,583,90),(117,583,91),(118,640,91),(119,300,285),(120,307,90),(121,500,80),(122,320,80),(123,1160,90),(124,1160,91),(125,600,70),(126,600,71),(127,210,70),(128,210,71),(129,1001,41),(130,1000,40),(131,77,357),(132,1000,60),(133,1075,113),(134,1076,133),(135,680,60),(136,848,300),(137,422,241),(138,873,322),(139,221,251),(140,220,250),(141,960,91),(142,196,75),(143,547,75),(144,546,75),(145,545,75),(146,195,75),(147,1030,100),(148,1031,100),(149,229,305),(150,230,305),(151,1050,90),(152,600,250),(153,600,120),(154,402,80),(155,225,125),(156,660,65),(157,235,251),(158,234,250),(159,489,69),(160,1925,272),(161,226,0),(162,227,91);
/*!40000 ALTER TABLE `Placements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Urls`
--

DROP TABLE IF EXISTS `Urls`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Urls` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `u_url` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Urls`
--

LOCK TABLES `Urls` WRITE;
/*!40000 ALTER TABLE `Urls` DISABLE KEYS */;
INSERT INTO `Urls` (`id`, `u_url`) VALUES (1,'http://www.trustnet.com'),(2,'http://www.trustnet.com/IMAUTOEICs.aspx'),(3,'http://www.trustnet.com/Investments/Perf.aspx?univ=O'),(4,'http://www.ftadviser.com/'),(5,'http://www.morningstar.co.uk/uk/'),(6,'http://www.pensions-expert.com'),(7,'http://www.professionaladviser.com'),(8,'http://www.citywire.co.uk/new-model-adviser'),(9,'http://www.citywire.co.uk/wealth-manager'),(10,'http://www.theguardian.com/uk'),(11,'http://www.theguardian.com/world'),(12,'http://www.ft.com/home/uk'),(13,'http://www.barrons.com/'),(14,'http://www.bloomberg.com/markets'),(15,'http://www.bloomberg.com/insights'),(16,'http://www.economist.com'),(17,'http://www.iii.co.uk'),(18,'http://www.moneywise.co.uk'),(19,'http://www.telegraph.co.uk'),(20,'http://www.moneyweek.com'),(21,'http://www.telegraph.co.uk/finance'),(22,'http://www.telegraph.co.uk/finance/personalfinance'),(23,'http://www.funds.telegraph.co.uk/clients/telegraph'),(25,'http://www.moneymarketing.co.uk/investments'),(26,'http://www.moneyobserver.com/how-to-invest'),(27,'https://www.fool.co.uk'),(28,'http://uk.reuters.com'),(30,'http://www.moneywise.co.uk/investing/first-time-investor/expert-investment-tips-50-to-50000'),(31,'http://www.moneywise.co.uk/investing/tax-efficient-investing'),(32,'http://www.moneywise.co.uk/investing/funds'),(33,'http://www.moneywise.co.uk/investing/investment-trusts'),(34,'http://www.moneysavingexpert.com'),(35,'http://www.theguardian.com/uk/money'),(36,'http://www.whatinvestment.co.uk'),(37,'https://www.boringmoney.co.uk'),(38,'http://www.etnet.com.hk/www/tc/home/index.php'),(39,'http://www.forbes.com/forbes/welcome'),(40,'http://www.dailymail.co.uk/home/index.html'),(41,'http://www.forbes.com');
/*!40000 ALTER TABLE `Urls` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-10-01 19:38:55
