---
counter: True
comment: True
---


# C++各种函数使用

!!! abstract
    这里归档一些C++函数的使用和扩展等



## std::string

### std::string::substr

```C++
string substr (size_t pos = 0, size_t len = npos) const;
```

返回一个新建的 初始化为string对象的子串的拷贝string对象。子串是，在字符位置pos开始，跨越len个字符（或直到字符串的结尾，以先到者为准）对象的部分。

??? example "应用"
    ```C++
    // string::substr
    #include <iostream>
    #include <string>

    int main () {
    std::string str="We think in generalities, but we live in details.";
                                            // (quoting Alfred N. Whitehead)
    std::string str2 = str.substr (3,5);     // "think"
    std::size_t pos = str.find("live");      // position of "live" in str
    std::string str3 = str.substr (pos);     // get from "live" to the end
    std::cout << str2 << ' ' << str3 << '\n';
    return 0;
    }
    ```

### std::string::find

```C++
size_t find (const string& str, size_t pos = 0) const noexcept;
size_t find (const char* s, size_t pos = 0) const;
size_t find (const char* s, size_t pos, size_type n) const;
size_t find (char c, size_t pos = 0) const noexcept;
```

返回值类型是`std::string::size_type (size_t)`， 对应的是查找对象在字符串中的位置（从0开始），如果未查找到，该返回值是一个很大的数据（4294967295），判断时与 `std::string::npos`进行对比。

**建议使用`size_type`，这样可以适应不同的平台。因为`int`类型的大小会根据不同平台而不同。**

??? example "应用"
    ```C++
    std::string str("abcdefg");
    std::string::size_type pos = str.find("abc");
    if (pos != std::string::npos) {
        cout << "Not find" << endl;
    }
    // or
    std::string str("abcdefg");
    if (str.find("abc") != std::string::npos) {
        cout << "Not find" << endl;
    }
    ```

??? note "扩展"
    - `s.find(t)`                   第一次出现的位置
    - `s.rfind(t)`                  最后一次出现的位置
    - `s.find_first_of(t)`          任何一个字符第一次出现的位置
    - `s.find_last_of(t)`           任何一个字符最后一次出现的位置
    - `s.find_first_not_of(t)`      第一个不在t中的字符所在位置
    - `s.find_last_not_of(t)`       最后一个不在t中的字符所在位置