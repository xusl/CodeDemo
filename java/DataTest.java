//package Demo;
import java.io.FileOutputStream;
import java.net.InetAddress;
import java.net.UnknownHostException;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.BufferedOutputStream;
import java.io.BufferedInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

public class DataTest {
    public static final String SHARE_RECEIVE_DIR = "ShareReceive";

    class Data {
        private String name;
        public Data(String name) {
            this.name = name;
        }

        public void setName(String name) { this.name = name; } 
        public Data clone() { return new Data(name); } 
        public String toString() { return name; }
    }

    public static String getFreeShareReceivedFileDir() {
        String mFreeShareReceivedDir = "." + File.separator + SHARE_RECEIVE_DIR;
        File file = new File(mFreeShareReceivedDir);

        if (!file.exists()) {
            file.mkdirs();
        }

        return mFreeShareReceivedDir;
    }

    public static File copyReceivedShareFile(String tempPath, String fileName) throws IOException {
        File src = new File(tempPath);
        int dot = fileName.lastIndexOf('.');
        String ext = "";
        String basename = fileName;
        String receiveDir = getFreeShareReceivedFileDir();
        File dst = new File(receiveDir + File.separator + fileName);

        if (dot >= 0) {
            ext = fileName.substring(dot);
            basename = fileName.substring(0, dot);
        }

        for (int i = 0; dst.isDirectory() || dst.exists(); i++){
            StringBuilder sb = new StringBuilder(receiveDir);
            sb.append(File.separator);
            sb.append(basename);
            sb.append('(');
            sb.append(i);
            sb.append(')');
            if (dot >= 0) {
                sb.append(ext);
            }
            dst = new File(sb.toString());
        }
        copy(src, dst);

        return dst;
    }

    public static void copy(File src, File dst) throws IOException {
        InputStream in = new BufferedInputStream(new FileInputStream(src));
        OutputStream out = new BufferedOutputStream(new FileOutputStream(dst));

        // Transfer bytes from in to out
        byte[] buf = new byte[1024];
        int len;
        while((len = in.read(buf)) > 0) {
            out.write(buf, 0, len);
        }
        in.close();
        out.close();
    }

    /*
    public static void threadPool() { 
        ThreadFactory namedThreadFactory = Executors.defaultThreadFactory();
        ExecutorService singleThreadPool = new ThreadPoolExecutor(1,
                1,
                0L,
                TimeUnit.MILLISECONDS,
                new LinkedBlockingQueue<Runnable>(1024),
                namedThreadFactory,
                new ThreadPoolExecutor.AbortPolicy());
        //        singleThreadPool.execute(()-> System.out.println(Thread.currentThread().getName()));

        singleThreadPool.shutdown();
    } 
    */


    static class MyComparator implements Comparator<Long> {

        @Override
        public int compare(Long o1, Long o2) {
            /*
               if (o1.isServer()) {
               return 1;
               }

               if (o2.isServer()) {
               return -1;
               }
               */

            if (o1 > o2) {
                return 1;
            }

            if (o1 < o2) {
                return -1;
            }

            return 0;
        }
    }


    private static void strip(String ssid) {
        System.out.println("origin:" + ssid);
        if (ssid.startsWith("\"")) {
            ssid = ssid.substring(1);
        }

        if (ssid.endsWith("\"")) {
            ssid = ssid.substring(0, ssid.length() - 1);
        }

        System.out.println("strip:" + ssid); 
    }


    public static void main(String[] args) { 
        List<Long> sortData = new ArrayList<>();
        sortData.add(9L);
        sortData.add(4L);
        sortData.add(3L);
        sortData.add(100L);
        sortData.add(96L);
        sortData.add(22L);
        sortData.add(33L); 
        sortData.add(11L); 
        sortData.add(10_000L); 

        strip("\"0012434534500\"");
        strip("0012434534500\"");
        strip("0012434534500");


        for(Long value : sortData) {
            System.out.printf(String.valueOf(value));
            System.out.printf(",");
        }

        System.out.println("\n=========================" + null);

        Collections.sort(sortData, new MyComparator());
        for(Long value : sortData) {
            System.out.printf(String.valueOf(value));
            System.out.printf(",");
        }

        System.out.println("\n=========================");


        Data foo = new DataTest().new Data("Hello World!");
        Data bar = foo;
        Data clone = foo.clone();

        System.out.printf("foo origin ///////////////////////////////:\n".replace('/', '-'));

        System.out.printf("foo origin:%s\n", foo.toString());
        System.out.printf("bar origin:%s\n", bar.toString());
        System.out.printf("clone origin:%s\n", clone.toString());

        bar.setName("Goodbye!");

        System.out.printf("foo now:%s\n", foo.toString());
        System.out.printf("bar now:%s\n", bar.toString());
        System.out.printf("clone now:%s\n", clone.toString());
        try {
            System.out.printf("Ip address:%s\n", InetAddress.getByName("/192.168.1.1").toString());
        } catch (UnknownHostException e) {
            e.printStackTrace();
        }
        int integrity[] = {1, 2, 3};
        for (int i : integrity) {
            System.out.print(String.valueOf(i));
        }

        try {
            copyReceivedShareFile("./temp.txt", "my.log");
            copyReceivedShareFile("./temp.txt", "my.log");
            copyReceivedShareFile("./temp.txt", "my.log");
            copyReceivedShareFile("./temp.txt", ".log");
            copyReceivedShareFile("./temp.txt", ".log");
            copyReceivedShareFile("./temp.txt", "log");
            copyReceivedShareFile("./temp.txt", "log");
            copyReceivedShareFile("./temp.txt", "log.");
            copyReceivedShareFile("./temp.txt", "log.");
        } catch (IOException e) {
            e.printStackTrace();
        }

        String testData = "HelloWorld!中国人يرجى اختيار الكميةን ይምረጡ<कृपया राशी चुनेंकृपया रकम चयन ерите сумму.براہ کرم رقمVui lòng chọn ";
        try {
            FileOutputStream fos = new FileOutputStream("temp.txt");
            fos.write(testData.getBytes());
            File testFile = new File("temp.txt");
            System.out.print("string length " + testData.length() +
                    ", string byte length"+ testData.getBytes().length +
                    ", file length" + testFile.length() +
                    "\n");
        } catch (IOException ioe) {
            System.out.print(ioe.getMessage());
        }

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
