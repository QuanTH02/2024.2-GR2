using System;

public class Calculator {
    public int Add(int a, int b) {
        return a + b;
    }
    
    public int Subtract(int a, int b) {
        return a - b;
    }
}
using System;
using System.Text;

public class StringUtils {
    public static string Reverse(string str) {
        if (str == null) return null;
        char[] charArray = str.ToCharArray();
        Array.Reverse(charArray);
        return new string(charArray);
    }
    
    public static bool IsEmpty(string str) {
        return string.IsNullOrEmpty(str);
    }
}
using System;
using System.Linq;

public class ArrayHelper {
    public static int[] Sort(int[] arr) {
        if (arr == null) return null;
        Array.Sort(arr);
        return arr;
    }
    
    public static int FindMax(int[] arr) {
        if (arr == null || arr.Length == 0) return -1;
        return arr.Max();
    }
}
using System;
using System.IO;

public class FileHandler {
    public static void WriteToFile(string filename, string content) {
        try {
            File.WriteAllText(filename, content);
        } catch (IOException e) {
            Console.WriteLine(e.Message);
        }
    }
    
    public static string ReadFromFile(string filename) {
        try {
            return File.ReadAllText(filename);
        } catch (IOException e) {
            Console.WriteLine(e.Message);
            return null;
        }
    }
}
using System;

public class MathUtils {
    public static double Power(double base, double exponent) {
        return Math.Pow(base, exponent);
    }
    
    public static int Factorial(int n) {
        if (n <= 1) return 1;
        return n * Factorial(n - 1);
    }
    
    public static bool IsPrime(int n) {
        if (n < 2) return false;
        for (int i = 2; i <= Math.Sqrt(n); i++) {
            if (n % i == 0) return false;
        }
        return true;
    }
}
