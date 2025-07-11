public class Calculator {
    public int add(int a, int b) {
        return a + b;
    }
    
    public int subtract(int a, int b) {
        return a - b;
    }
}
public class StringUtils {
    public static String reverse(String str) {
        if (str == null) return null;
        return new StringBuilder(str).reverse().toString();
    }
    
    public static boolean isEmpty(String str) {
        return str == null || str.length() == 0;
    }
}
public class ArrayHelper {
    public static int[] sort(int[] arr) {
        if (arr == null) return null;
        Arrays.sort(arr);
        return arr;
    }
    
    public static int findMax(int[] arr) {
        if (arr == null || arr.length == 0) return -1;
        return Arrays.stream(arr).max().getAsInt();
    }
}
public class FileHandler {
    public static void writeToFile(String filename, String content) {
        try (FileWriter writer = new FileWriter(filename)) {
            writer.write(content);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    public static String readFromFile(String filename) {
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            return reader.lines().collect(Collectors.joining("\n"));
        } catch (IOException e) {
            e.printStackTrace();
            return null;
        }
    }
}
public class MathUtils {
    public static double power(double base, double exponent) {
        return Math.pow(base, exponent);
    }
    
    public static int factorial(int n) {
        if (n <= 1) return 1;
        return n * factorial(n - 1);
    }
    
    public static boolean isPrime(int n) {
        if (n < 2) return false;
        for (int i = 2; i <= Math.sqrt(n); i++) {
            if (n % i == 0) return false;
        }
        return true;
    }
}
