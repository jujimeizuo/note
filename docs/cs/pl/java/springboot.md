---
counter: true
comment: true
---

# SpringBoot

!!! abstract
    当初为了做数据库课设，让牌王花了 1.5h 教我 springboot 入门，之前写在 csdn 上，现在移到 note 里


首先创建一个springboot项目。
****

## model层
model层也叫pojo层或者entity层，个人比较喜欢pojo层。
一般数据库的一张表对应一个pojo层，并且表中所有字段都在pojo层都一一对应。

eg：一张Goods表

<center><img src="https://cdn.jujimeizuo.cn/blog/2021/02/202102201819220.png"></center>

然后要先建一个pojo的package，代表它是实体层。
再在该package下创建一个Goods的java文件，创建的对象都是和表里字段一一对应，如下所示：

```java
package pojo;

import lombok.*;

@Data
public class Goods {
    /*
    商品编号
     */
    private String GNo;

    /*
    商品名称
     */
    private String GName;

    /*
    商品价格
     */
    private Double GPrice;
}
```
这里的lombok的作用时为了简化代码，因为对于private这样的对象，想要调用它的时候，需要get和set两个方法，而有了lombok之后就可以不用写，直接用即可。
不过要添加依赖和注解@Data，lombok还有很多其他用法，之后可能会出一篇博客。

通过maven下载依赖：

```java
<dependency>
	<groupId>org.projectlombok</groupId>
	<artifactId>lombok</artifactId>
	<optional>true</optional>
</dependency>
```
这样数据库里的字段，我们就可以用对象来表示。

****
但是model不属于springboot的三层框架。
主要说明是dao层、service层和controller层。
这些已经是属于后端了。

对于一个项目，安全性是非常有必要的，所以springboot很好地体现了这一点。

比如：
想要访问数据库并且操作，只能通过dao层向数据库发送sql语句，将这些结果通过接口传给service层。
想要处理数据，要先向dao层请求数据，对dao层传过来的数据进行加工处理，将这些处理好的数据通过接口传给controller层。
客户想要查询或修改数据时，要先向service层请求数据，收集service层传过来的数据，将这些数据通过接口显示给客户，一般通过html等方法给客户。
下面会一一说明。
****

## dao层

dao层也叫mapper层，数据持久层，个人比较喜欢mapper层。
对数据库进行持久化操作，他的方法是针对数据库操作的，基本用到的就是增删改查。它只是个接口，只有方法名字，具体实现在mapper.xml中。

既然mapper层是直接与数据库相挂钩的，所以要先连接数据库。
可以在sqlMapConfig.xml文件或者application.properties文件里添加数据库属性等，如下所示：

- sqlMapConfig.xml添加属性：

```java
<!-- 加载属性文件 -->
<properties resource="/config/db.properties"></properties>

<!-- 和spring整合后environment配置将废除 -->
<environments default="development">
    <environment id="development">
        <!-- 使用jdbc事务管理 -->
        <transactionManager type="JDBC" />
        <!-- 数据库连接池,由mybatis管理 -->
        <dataSource type="POOLED">
            <property name="driver" value="${jdbc.driver}" />
            <property name="url" value="${jdbc.url}" />
            <property name="username" value="${jdbc.username}" />
            <property name="password" value="${jdbc.password}" />
        </dataSource>
    </environment>
</environments>
```
在 SqlMapConfig.xml就不需要对数据库连接参数硬编码。 

- application.properties添加属性：

<center><img src="https://cdn.jujimeizuo.cn/blog/2021/02/20210220185731148.png"></center>


方便对参数进行统一管理，其他 xml 可以应用该配置文件。

然后检查是否连上数据库，请看下图：


<center><img src="https://cdn.jujimeizuo.cn/blog/2021/02/20210220185938611.png"></center>

然后自己配置数据库。

数据库连接上了，到了两个文件的编写，我采用mybatis框架。

如何编写mapper.xml，对数据库增删改查？

**在学习MyBatis框架的过程中，发现在idea里面没法创建Mapper.xml映射文件，创建出的xml文件没有Mapper.xml文件的基本格式，下面说明如何在idea中创建Mapper.xml映射文件模板。**

File → Settings… → Editor → File and Code Templates

<center><img src="https://cdn.jujimeizuo.cn/blog/2021/02/20210220190615764.jpg"></center>

<center><img src="https://cdn.jujimeizuo.cn/blog/2021/02/20210220190739783.png"></center>

点击"+"号，并输入文件的名称和文件的类型，编辑好模板后点击Apply即可创建成功}
<center><img src="https://cdn.jujimeizuo.cn/blog/2021/02/20210220190846808.png"></center>

<center><img src="https://cdn.jujimeizuo.cn/blog/2021/02/20210220190913559.png"></center>

**mapper.xml文件模版**

```java
<?xml version="1.0" encoding="utf-8" ?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" 
"http://mybatis.org/dtd/mybatis-3-mapper.dtd" >
<mapper namespace="">
    
</mapper>


```

创建GoodsMapper.xml文件。

<center><img src="https://cdn.jujimeizuo.cn/blog/2021/02/20210220191221241.png"></center>

编写内容：

```java
<?xml version="1.0" encoding="utf-8" ?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN"
        "http://mybatis.org/dtd/mybatis-3-mapper.dtd" >
<mapper namespace="mapper.GoodsMapper">
    <!--增加商品-->
    <insert id="insertGoods" parameterType="mapper.GoodsMapper">
        insert into Goods(GNo, GName, GPrice) values(#{GNo},#{GName},#{GPrice})
    </insert>

    <!--删除商品-->
    <delete id="deleteGoods" parameterType="java.String">
        delete from Goods where id=#{id}
    </delete>

    <!--修改商品-->
    <update id="uodateGoods" parameterType="mapper.GoodsMapper">
        update Goods set GNo=#{GNo}, GName=#{GName}, GPrice=#{GPrice} where id=#{id}
    </update>

    <!--查找商品-->
    <select id="findGoods" parameterType="java.String" resultType="mapper.GoodsMapper">
        select *from Goods where id=#{id}
    </select>
</mapper>
```

创建GoodsMapper的接口。

```java
package mapper;

import pojo.Goods;

public interface GoodsMapper {
    /**
     *增加商品
     * @param goods
     * @throw Exception
     */
    void insertGoods(Goods goods) throws Exception;
    /**
     * 删除商品
     * @param GNo
     * @throw Exception
     */
    void deleteGoods(String GNo) throws Exception;
    /**
     * 修改商品
     * @param goods
     * @throw Exception
     */
    void updateGoods(Goods goods) throws Exception;
    /**
     * 根据GNo查找
     * @return
     * @throw Exception
     */
    Goods findByGNo(String GNo) throws Exception;
}
```
不需要编写接口对实现类了，只要这两个文件的映射关系对应好就ok，这不在本文的讲述范围内。
****
## service层
service层叫业务逻辑层，存放业务逻辑处理，不直接对数据库进行操作，有接口和接口实现类，提供controller层调用的方法。

创建两个文件，一个存放接口类，一个存放接口实现类。

GoodsService接口类：

```java
package service.Goods;

import pojo.Goods;

public interface GoodsService {
    void insertGoods(Goods goods) throws Exception;
    void deleteGoods(String GNo) throws Exception;
    void updateGood(Goods goods) throws Exception;
    void findByGNo(String GNo) throws Exception;
}
```

GoodsServiceImpl接口实现类：

```java
package service.Goods;

import mapper.GoodsMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import pojo.Goods;

@Service
public class GoodsServiceImpl implements GoodsService {
    @Autowired
    private GoodsMapper goodsMapper;

    @Override
    public void insertGoods(Goods goods) throws Exception {
        goodsMapper.insertGoods(goods);
    }

    @Override
    public void deleteGoods(String GNo) throws Exception {
        goodsMapper.deleteGoods(GNo);
    }

    @Override
    public void updateGood(Goods goods) throws Exception {
        goodsMapper.updateGoods(goods);
    }

    @Override
    public void findByGNo(String GNo) throws Exception {
        goodsMapper.findByGNo(GNo);
    }
}

```

**就这样，service层与mapper层建立起了联系，service层可以调用mapper层的方法。**

****

## controller层

controller层叫控制器层，负责前后端交互，接受前端请求，调用service层，接收service层返回的数据，最后返回具体的页面和数据到客户端。

同样，也需要两个文件，接口类和接口实现类。

GoodsControllerI接口类：

```java
package Controller.Goods;

import pojo.Goods;

public interface GoodsController {
    void insertGoods(Goods goods) throws Exception;
    void deleteGoods(String GNo) throws Exception;
    void updateGood(Goods goods) throws Exception;
    void findByGNo(String GNo) throws Exception;
}
```

GoodsControllerImpl接口实现类：

```java
package Controller.Goods;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import pojo.Goods;
import service.Goods.GoodsService;

@Controller
public class GoodsControllerImpl {
    @Autowired
    private GoodsService goodsService;

    @RequestMapping(value = "/index")
    public String insertGoods(Goods goods) throws Exception {
        goodsService.insertGoods(goods);
        return "/index";
    }
    
    @RequestMapping(value = "/index")
    public String deleteGoods(String GNo) throws Exception {
        goodsService.deleteGoods(GNo);
        return "/index";
    }
    
    @RequestMapping(value = "/index")
    public String updateGoods(Goods goods) throws Exception {
        goodsService.updateGood(goods);
        return "/index";
    }
    
    @RequestMapping(value = "/index")
    public String findByGNo(String GNo) throws Exception {
        Goods goods = new Goods();
        goods = goodsService.findByGNo(GNo);
        return "/index";
    }
}
```

这样，客户可以通过请求的方式，将数据从前端传给Controller层，然后一层一层传下去，在一层一层地传上来，实现了后端开发。

是不是发现和前端没什么关系？
是的，springboot还有一个优点就是实现了前后端分离，从而工作人员分配任务的时候更加具有条理性。而三层的架构可以让程序员很快地知道bug出现在哪里，哪一层，哪一文件，很快的修改bug。

**呜呼，总而言之，springboot作为web开发的一个主流框架，正式因为这些优秀点让它脱颖而出。**

**这一篇写得好累。**