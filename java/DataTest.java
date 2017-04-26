package Demo;

public class DataTest {
    class Data {
        private String name;
        public Data(String name) {
            this.name = name;
        }

        public void setName(String name) { this.name = name; } 
        public Data clone() { return new Data(name); } 
        public String toString() { return name; }
    }

    public static void main(String[] args) { 
        Data foo = new DataTest().new Data("Hello World!");
        Data bar = foo;
        Data clone = foo.clone();

        System.out.printf("foo origin:%s\n", foo.toString());
        System.out.printf("bar origin:%s\n", bar.toString());
        System.out.printf("clone origin:%s\n", clone.toString());

        bar.setName("Goodbye!");

        System.out.printf("foo now:%s\n", foo.toString());
        System.out.printf("bar now:%s\n", bar.toString());
        System.out.printf("clone now:%s\n", clone.toString());
    }
}



















/*
            //return new Data(new String(name));
        String foo = "Hello World!";
        String reference = foo;
        String copy = new String(foo);
        copy.append("!");
        System.out.printf("foo :%s\n", foo);
        System.out.printf("copy :%s\n", copy);
        reference.append(".");
        System.out.printf("foo :%s\n", foo);
        System.out.printf("reference:%s\n", reference);
*/
