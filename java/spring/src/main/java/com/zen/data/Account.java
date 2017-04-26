package com.zen.data;

public class Account {
    private Long id;
    private String name;
    public Account() {
        super();
    }
    public Account(String name, Long id) {
        this();
        this.name = name;
        this.id = id;
    }

    public Long getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public void setName(String name) {
        this.name = name;
    }
}
