---
counter: true
comment: true
---

# 设计模式

> **设计模式**是软件设计中常见问题的典型解决方案。他们就想能根据需求进行调整的预制蓝图，可用于解决代码中反复出现的设计问题。

> 设计模式与方法或库的使用方式不同，你很难直接在自己的程序中套用某个设计模式。模式并不是一段特定的代码，而是解决特定问题的一般性概念。 你可以根据模式来实现符合自己程序实际所需的解决方案。

> 人们常常会混淆模式和算法，因为两者在概念上都是已知特定问题的典型解决方案。 但算法总是明确定义达成特定目标所需的一系列步骤，而模式则是对解决方案的更高层次描述。同一模式在两个不同程序中的实现代码可能会不一样。

> 算法更像是菜谱：提供达成目标的明确步骤。而模式更像是蓝图：你可以看到最终的结果和模式的功能，但需要自己确定实现步骤。

!!! abstract
    归档学习设计模式时的一些笔记
    
    主要用 C++ 实现，持续更新中



## 创建型模式

### 抽象工厂模式

#### 概述
**抽象工厂模式**是一种创建型设计模式， 它能创建一系列相关的对象， 而无需指定其具体类。

#### 应用场景
1. 如果代码需要与多个不同系列的相关产品交互，但是由于无法提前获取相关信息，或者出于对未来扩展性的考虑，你不希望代码基于产品的具体类进行构建，在这种情况下，你可以使用抽象工厂。

2. 如果你有一个基于一组抽象方法的累，且其主要功能因此变得不明确，那么在这种情况下可以考虑了使用抽象工厂模式

#### 优缺点

##### 优点
- 你可以确保同一工厂生产的产品相互匹配
- 你可以避免客户端和具体产品代码的耦合
- 单一职责原则。你可以将产品生成代码抽取到同一位置，使得代码易于维护
- 开闭原则。向应用程序中引入新产品变体时，你无需修改客户端代码

##### 缺点
- 由于采用该模式需要向应用中引入众多接口和类，代码可能会比之前更加复杂

??? note "AbstractFactory.cpp"
    ```C++
    #include <iostream>
    #include <string>

    class AbstractProductA {
    public :
        virtual ~AbstractProductA() {};
        virtual std::string UsefulFunctionA() const = 0;
    };

    class ConcreteProductA1 : public AbstractProductA {
    public :
        std::string UsefulFunctionA() const override {
            return "The result of the product A1.";
        }
    };

    class ConcreteProductA2 : public AbstractProductA {
    public :
        std::string UsefulFunctionA() const override {
            return "The result of the product A2.";
        }
    };

    class AbstractProductB {
    public :
        virtual ~AbstractProductB() {};
        virtual std::string UsefulFunctionB() const = 0;
        virtual std::string AnotherUsefulFunctionB(const AbstractProductA &collaborator) const = 0;
    };

    class ConcreteProductB1 : public AbstractProductB {
    public :
        std::string UsefulFunctionB() const override {
            return "The result of the product B1.";
        }

        std::string AnotherUsefulFunctionB(const AbstractProductA &collaborator) const override {
            const std::string result = collaborator.UsefulFunctionA();
            return "The result of the B1 collaborating with ( " + result + " )";
        }
    };

    class ConcreteProductB2 : public AbstractProductB {
    public :
        std::string UsefulFunctionB() const override {
            return "The result of the product B2.";
        }

        std::string AnotherUsefulFunctionB(const AbstractProductA &collaborator) const override {
            const std::string result = collaborator.UsefulFunctionA();
            return "The result of the B2 collaborating with ( " + result + " )";
        }
    };


    class AbstractFactory {
    public :
        virtual AbstractProductA *CreateProductA() const = 0;
        virtual AbstractProductB *CreateProductB() const = 0;
    };

    class ConcreteFactory1 : public AbstractFactory {
    public :
        AbstractProductA *CreateProductA() const override {
            return new ConcreteProductA1();
        }
        AbstractProductB *CreateProductB() const override {
            return new ConcreteProductB1();
        }
    };

    class ConcreteFactory2 : public AbstractFactory {
    public :
        AbstractProductA *CreateProductA() const override {
            return new ConcreteProductA2();
        }
        AbstractProductB *CreateProductB() const override {
            return new ConcreteProductB2();
        }
    };

    void ClientCode(const AbstractFactory &factory) {
        const AbstractProductA *product_A = factory.CreateProductA();
        const AbstractProductB *product_B = factory.CreateProductB();
        std::cout << product_B -> UsefulFunctionB() << "\n";
        std::cout << product_B -> AnotherUsefulFunctionB(*product_A) << "\n";
        delete product_A;
        delete product_B;
    }

    int main() {
        std::cout << "Client: Testing client code with the first factory type:\n";
        ConcreteFactory1 *f1 = new ConcreteFactory1();
        ClientCode(*f1);
        delete f1;
        std::cout << std::endl;
        std::cout << "Client: Testing the same client code with the second factory type:\n";
        ConcreteFactory2 *f2 = new ConcreteFactory2();
        ClientCode(*f2);
        delete f2;
        return 0;
    }
    ```

### 工厂方法模式

#### 概述
**工厂方法模式**是一种创建型设计模式，其在父类中提供一个创建对象的方法，允许子类决定实例化对象的类型。

#### 应用场景
1. 编写代码的过程中，如果无法预知对象确切类别以及依赖关系时，可使用工厂方法

2. 如果你希望用户能够扩展你软件库或框架的内部组件，可使用工厂方法

3. 如果你希望复用现有对象来节省系统资源，而不是每次都重新创建对象，可使用工厂方法

#### 优缺点
##### 优点
- 可以避免创建者和具体产品之间的紧密耦合
- 单一职责原则。你可以将产品创建代码放在程序的单一位置，从而使得代码更容易维护
- 开闭原则。无需更改现有客户端代码，你就可以在程序中引入新的产品类型
##### 缺点
- 应用工厂方法模式需要引入许多新的子类，代码可能会变得复杂。最好的情况时将该模式引入创建者类的现有层次结构中

??? note "FactoryMethod.cpp"
    ```C++
    #include <iostream>

    class Product {
    public :
        virtual ~Product() {}
        virtual std::string Operation() const = 0;
    };

    class ConcreteProduct1 : public Product {
    public :
        std::string Operation() const override {
            return "{Result of the ConcreteProduct1}";
        }
    };

    class ConcreteProduct2 : public Product {
    public :
        std::string Operation() const override {
            return "{Result of the ConcreteProduct2}";
        }
    };

    class Creator {
    public :
        virtual ~Creator() {};
        virtual Product* FactoryMethod() const = 0;

        std::string SomeOperation() const {
            Product* product = this -> FactoryMethod();
            std::string result = "Creator: The same creator's code has just worked with " + product->Operation();
            delete product;
            return result;
        }
    };

    class ConcreteCreator1 : public Creator {
    public :
        Product* FactoryMethod() const override {
            return new ConcreteProduct1();
        }
    };

    class ConcreteCreator2 : public Creator {
    public :
        Product* FactoryMethod() const override {
            return new ConcreteProduct2();
        }
    };

    void ClientCode(const Creator& creator) {
        std::cout << "Client: I'm not aware of the creator's class, but it still works.\n" << creator.SomeOperation() << std::endl;
    }

    int main() {
        std::ios::sync_with_stdio(false);
        std::cin.tie(nullptr);

        std::cout << "App: Launched with the ConcreteCreator1.\n";
        Creator* creator1 = new ConcreteCreator1();
        ClientCode(*creator1);
        std::cout << std::endl;
        std::cout << "App: Launched with the ConcreteCreator2.\n";
        Creator* creator2 = new ConcreteCreator2();
        ClientCode(*creator2);

        delete creator1;
        delete creator2;

        return 0;
    }
    ```

### 生成器模式

#### 概述
**生成器模式**是一种创建型设计模式， 使你能够分步骤创建复杂对象。该模式允许你使用相同的创建代码生成不同类型和形式的对象。

#### 应用场景
1. 使用生成器模式可避免“重叠构造函数”的出现
2. 当你希望使用代码创建不同形式的产品（例如石头或木头房屋）时，可使用生成器模式
3. 使用生成器构造组合树或其他复杂对象

#### 优缺点

##### 优点
- 你可以分步创建对象，暂缓创建步骤或递归运行创建步骤
- 生成不同形式的产品时，你可以复用相同的制造代码
- 单一职责原则。你可以将复杂构造代码从产品的业务逻辑中分离出来

##### 缺点
- 由于该模式需要新增多个类，因此代码整体复杂程度会有所增加

??? note "Builder.cpp"
    ```C++
    #include <iostream>
    #include <string>
    #include <vector>
    class Product1 {
    public :
        std::vector<std::string> parts;
        void ListParts() const {
            std::cout << "Product parts: ";
            for(size_t i = 0;i < parts.size(); i++) {
                std::cout << parts[i] << " \n"[i == parts.size() - 1];
            }
            std::cout << "\n";
        }
    };

    class Builder {
    public :
        virtual ~Builder() {}
        virtual void ProducePartA() const = 0;
        virtual void ProducePartB() const = 0;
        virtual void ProducePartC() const = 0;
    };

    class ConcreteBuilder1 : public Builder {
    private :
        Product1* product;

    public :
        ConcreteBuilder1() { this -> Reset(); }
        ~ConcreteBuilder1() { delete product; }
        void Reset() { this -> product = new Product1(); }

        void ProducePartA() const override {
            this -> product -> parts.push_back("PartA1");
        }
        void ProducePartB() const override {
            this -> product -> parts.push_back("PartB1");
        }
        void ProducePartC() const override {
            this -> product -> parts.push_back("PartC1");
        }

        Product1* GetProduct() {
            Product1* result = this -> product;
            this -> Reset();
            return result;
        }
    };

    class Director {
    private :
        Builder* builder;

    public :
        void set_builder(Builder* builder) {
            this -> builder = builder;
        }

        void BuildMinimalViableProduct() {
            this -> builder -> ProducePartA();
        }

        void BuildFullFeaturedProduct() {
            this -> builder -> ProducePartA();
            this -> builder -> ProducePartB();
            this -> builder -> ProducePartC();
        }
    };

    void ClientCode(Director& director) {
        ConcreteBuilder1* builder = new ConcreteBuilder1();
        director.set_builder(builder);
        std::cout << "Standard basic product: \n";
        director.BuildMinimalViableProduct();

        Product1* p = builder -> GetProduct();
        p -> ListParts();
        delete p;

        std::cout << "Standard full featured product: \n";
        director.BuildFullFeaturedProduct();

        p = builder -> GetProduct();
        p -> ListParts();
        delete p;

        std::cout << "Custom product: \n";
        builder -> ProducePartA();
        builder -> ProducePartB();
        p = builder -> GetProduct();
        p -> ListParts();
        delete p;

        delete builder;
    }

    int main() {
        std::ios::sync_with_stdio(false);
        std::cin.tie(nullptr);

        Director* director = new Director();
        ClientCode(*director);
        delete director;

        return 0;
    }
    ```

### 原型模式

#### 概述
**原型模式**是一种创建型设计模式， 使你能够复制已有对象， 而又无需使代码依赖它们所属的类。

#### 应用场景
1. 如果你需要复制一些对象，同时又希望代码独立于这些对象所属的具体类，可以使用原型模式

2. 如果子类的区别仅在于其对象的初始化方式，那么你可以使用该模式来减少子类的数量。别人创建这些子类的目的可能是为零创建特定类型的对象

#### 优缺点

##### 优点
- 你可以克隆对象，而无需与它们所属的具体类相耦合
- 你可以克隆预生成原型，避免反复运行初始化代码
- 你可以更方便地生成复杂对象
- 你可以用继承以外的方式来处理复杂对象的不同配置

##### 缺点
- 克隆包含循环引用的复杂对象可能会非常麻烦

??? note "Prototype.cpp"
    ```C++
    #include <iostream>
    #include <string>
    #include <unordered_map>

    enum Type {
        PROTOTYPE_1 = 0, 
        PROTOTYPE_2
    };

    class Prototype {
    protected :
        std::string prototype_name_;
        float prototype_field_;

    public :
        Prototype() {}
        Prototype(std::string prototype_name) : prototype_name_(prototype_name) {}
        virtual ~Prototype() {}
        virtual Prototype *Clone() const = 0;
        virtual void Method(float prototype_field) {
            this -> prototype_field_ = prototype_field;
            std::cout << "Call Method from " << prototype_name_ << " with field : " << prototype_field << std::endl;
        }
    };

    class ConcretePrototype1 : public Prototype {
    private :
        float concrete_prototype_field1_;

    public :
        ConcretePrototype1(std::string prototype_name, float concrete_prototype_field) 
            : Prototype(prototype_name), concrete_prototype_field1_(concrete_prototype_field) {}

        Prototype *Clone() const override {
            return new ConcretePrototype1(*this);
        }
    };

    class ConcretePrototype2 : public Prototype {
    private :
        float concrete_prototype_field2_;

    public :
        ConcretePrototype2(std::string prototype_name, float concrete_prototype_field) 
            : Prototype(prototype_name), concrete_prototype_field2_(concrete_prototype_field) {}

        Prototype *Clone() const override {
            return new ConcretePrototype2(*this);
        }
    };

    class PrototypeFactory {
    private :
        std::unordered_map<Type, Prototype *, std::hash<int>> prototypes_;

    public :
        PrototypeFactory() {
            prototypes_[Type::PROTOTYPE_1] = new ConcretePrototype1("PROTOTYPE_1 ", 50.f);
            prototypes_[Type::PROTOTYPE_2] = new ConcretePrototype2("PROTOTYPE_2 ", 60.f);
        }

        ~PrototypeFactory() {
            delete prototypes_[Type::PROTOTYPE_1];
            delete prototypes_[Type::PROTOTYPE_2];
        }

        Prototype *CreatePrototype(Type type) {
            return prototypes_[type] -> Clone();
        }
    };

    void Client(PrototypeFactory &prototype_factory) {
        std::cout << "Let's create a Prototype 1\n";

        Prototype *prototype = prototype_factory.CreatePrototype(Type::PROTOTYPE_1);
        prototype -> Method(90);
        delete prototype;

        std::cout << "\n";

        std::cout << "Let's create a Prototype 2 \n";

        prototype = prototype_factory.CreatePrototype(Type::PROTOTYPE_2);
        prototype -> Method(10);

        delete prototype;
    }

    int main() {
        std::ios::sync_with_stdio(false);
        std::cin.tie(nullptr);

        PrototypeFactory *prototype_factory = new PrototypeFactory();
        Client(*prototype_factory);
        delete prototype_factory;	

        return 0;
    }
    ```

### 单例模式

#### 概述
**单例模式**是一种创建型设计模式，让你能够保证一个类只有一个实例，并提供一个访问该实例的全局节点。

#### 应用场景
1. 如果程序中的某个类对于所有客户端只有一个可用的实例，可以使用单例模式
2. 如果你需要更加严格地控制全局变量，可以使用单例模式

#### 优缺点
##### 优点
- 你可以保证一个类只有一个实例
- 你获得了一个指向该实例的全局访问节点
- 仅在首次请求单例对象时对其进行初始化

##### 缺点
- 违反了单一职责原则。该模式同时解决了两个问题
- 单例模式可能掩盖不良设计，比如程序各组件之间互相了解过多等
- 该模式在多线程环境下需要进行特殊处理，避免多个线程多次创建单例对象
- 单例的客户端代码单元测试可能会比较困难，因为许多测试框架以基于继承的方式创建模拟对象。由于单例类的构造函数是私有的，而且绝大部分语言无法重写静态方法，所以你需要想出仔细考虑模拟单例的方法。要么干脆不编写测试代码，或者不使用单例模式

??? note "Singleton.cpp"
    ```C++
    #include <iostream>
    #include <string>
    #include <thread>

    class Singleton {
    protected :
        Singleton(const std::string value) : value_(value) {}
        static Singleton* singleton_;
        std::string value_;

    public :
        Singleton(Singleton &other) = delete;
        
        void operator=(const Singleton &) = delete;
        
        static Singleton *GetInstance(const std::string& value);

        void SomeBusinessLogic() {}

        std::string value() const {
            return value_;
        }
    };

    Singleton* Singleton::singleton_ = nullptr;

    Singleton *Singleton::GetInstance(const std::string& value) {
        if(singleton_ == nullptr) {
            singleton_ = new Singleton(value);
        }
        return singleton_;
    }

    void ThreadFoo() {
        std::this_thread::sleep_for(std::chrono::milliseconds(1000));
        Singleton* singleton = Singleton::GetInstance("FOO");
        std::cout << singleton -> value() << "\n";
    }

    void ThreadBar() {
        std::this_thread::sleep_for(std::chrono::milliseconds(1000));
        Singleton* singleton = Singleton::GetInstance("BAR");
        std::cout << singleton -> value() << "\n";
    }

    int main() {
        std::ios::sync_with_stdio(false);
        std::cin.tie(nullptr);

        std::cout <<"If you see the same value, then singleton was reused (yay!\n" <<
                    "If you see different values, then 2 singletons were created (booo!!)\n\n" <<
                    "RESULT:\n";   	

        std::thread t1(ThreadFoo);
        std::thread t2(ThreadBar);
        t1.join();
        t2.join();
        
        return 0;
    }
    ```

## 结构型模式

### 适配器模式

#### 概述
**适配器模式**是一种结构型设计模式， 它能使接口不兼容的对象能够相互合作。

#### 应用场景
1. 当你希望使用某个类，但是其接口与其他代码不兼容时，可以使用适配器类
2. 如果你需要复用这样一些类，他们处于同一继承体系，并且它们又有了额外的一些共同的方法，但是这些共同的方法不是所有在这一继承体系中的子类所具有的共性

#### 优缺点

##### 优点
- 单一职责原则。你可以将接口或数据转换代码从程序主要也要业务逻辑中分离
- 开闭原则。只要客户端代码通过客户端接口与适配器进行交互，你就能在不修改现有客户端代码的情况下在程序中添加新类型的适配器

##### 缺点
- 代码整体复杂度增加，因为你需要新增一系列接口和类。有时直接更改服务类使其与其他代码兼容会更简单

??? note "Adapter.cpp"
    ```C++
    #include <iostream>
    #include <string>
    #include <algorithm>

    class Target {
    public :
        virtual ~Target() = default;

        virtual std::string Request() const {
            return "Target: The defaut target's behabior.";
        }
    };

    class Adaptee {
    public :
        std::string SpecificRequest() const {
            return ".eetpadA eht fo roivaheb laicepS";
        }
    };

    class Adapter : public Target {
    private :
        Adaptee *adaptee_;

    public :
        Adapter(Adaptee *adaptee) : adaptee_(adaptee) {}
        std::string Request() const override {
            std::string to_reverse = this -> adaptee_ -> SpecificRequest();
            std::reverse(to_reverse.begin(), to_reverse.end());
            return "Adapter: (TRANSLATED) " + to_reverse;
        }
    };

    void ClientCode(const Target *target) {
        std::cout << target -> Request();
    }

    int main() {
        std::ios::sync_with_stdio(false);
        std::cin.tie(nullptr);

        std::cout << "Client: I can work just fine with the Target objects:\n";
        Target *target = new Target;
        ClientCode(target);
        std::cout << "\n\n";
        Adaptee *adaptee = new Adaptee;
        std::cout << "Client: The Adaptee class has a weird interface. See, I don't understand it:\n";
        std::cout << "Adaptee: " << adaptee -> SpecificRequest();
        std::cout << "\n\n";
        std::cout << "Client: But I can work with it via the Adapter:\n";
        Adapter *adapter = new Adapter(adaptee);
        ClientCode(adapter);
        std::cout << "\n";

        delete target;
        delete adaptee;
        delete adapter;

        return 0;
    }
    ```

## 行为模式