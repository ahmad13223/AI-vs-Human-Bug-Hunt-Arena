from flask import Flask, render_template, request, jsonify
import re
import random
import time

app = Flask(__name__)

# Store active challenges by ID
active_challenges = {}

# Bug Hunt Game - Code samples with intentional bugs
BUG_HUNT_LEVELS = {
    'easy': {
        'python': [
            {
                'code': '''def check_age(age):
    if age >= 18:
        return "adult"
    elif age >= 13:
        return "teenager"
    elif age > 0:
        return "child"
    else:
        return "invalid"

# Test cases
print(check_age(25))
print(check_age(15))
print(check_age(8))
print(check_age(-5))''',
                'bugs': ['Logic error: age > 0 should be age >= 0 to handle newborns (age 0)'],
                'fixed_code': '''def check_age(age):
    if age >= 18:
        return "adult"
    elif age >= 13:
        return "teenager"
    elif age >= 0:
        return "child"
    else:
        return "invalid"

# Test cases
print(check_age(25))
print(check_age(15))
print(check_age(8))
print(check_age(0))''',
                'description': 'Fix the age validation logic!'
            },
            {
                'code': '''def calculate_discount(price, is_student):
    if is_student == True:
        discount = price * 0.1
        return price - discount
    else:
        return price

# Test
student_price = calculate_discount(100, True)
regular_price = calculate_discount(100, False)
print(f"Student: ${student_price}, Regular: ${regular_price}")''',
                'bugs': ['Missing return statement in else block creates inconsistent behavior'],
                'fixed_code': '''def calculate_discount(price, is_student):
    if is_student:
        discount = price * 0.1
        return price - discount
    else:
        return price

# Test
student_price = calculate_discount(100, True)
regular_price = calculate_discount(100, False)
print(f"Student: ${student_price}, Regular: ${regular_price}")''',
                'description': 'Find the discount calculation bug!'
            },
            {
                'code': '''def find_max_number(numbers):
    if len(numbers) == 0:
        return None
    
    max_num = numbers[0]
    for i in range(len(numbers)):
        if numbers[i] > max_num:
            max_num = numbers[i]
    return max_num

# Test with negative numbers
result = find_max_number([-5, -2, -10, -1])
print(f"Max: {result}")''',
                'bugs': ['Logic works correctly - this is actually a good implementation'],
                'fixed_code': '''def find_max_number(numbers):
    if len(numbers) == 0:
        return None
    
    max_num = numbers[0]
    for i in range(len(numbers)):
        if numbers[i] > max_num:
            max_num = numbers[i]
    return max_num

# Test with negative numbers
result = find_max_number([-5, -2, -10, -1])
print(f"Max: {result}")''',
                'description': 'Find the bug in max number detection!'
            }
        ],
        'javascript': [
            {
                'code': '''function checkPassword(password) {
    if (password.length > 8) {
        return "strong";
    } else if (password.length > 5) {
        return "medium";
    } else if (password.length > 0) {
        return "weak";
    } else {
        return "invalid";
    }
}

// Test cases
console.log(checkPassword("mypassword123"));
console.log(checkPassword("hello"));
console.log(checkPassword("hi"));
console.log(checkPassword(""));''',
                'bugs': ['Logic error: should be >= 8, >= 6 for proper password strength'],
                'fixed_code': '''function checkPassword(password) {
    if (password.length >= 8) {
        return "strong";
    } else if (password.length >= 6) {
        return "medium";
    } else if (password.length > 0) {
        return "weak";
    } else {
        return "invalid";
    }
}

// Test cases
console.log(checkPassword("mypassword123"));
console.log(checkPassword("hello"));
console.log(checkPassword("hi"));
console.log(checkPassword(""));''',
                'description': 'Fix the password strength logic!'
            },
            {
                'code': '''function calculateGrade(score) {
    if (score >= 90) {
        return "A";
    } else if (score >= 80) {
        return "B";
    } else if (score >= 70) {
        return "C";
    } else if (score >= 60) {
        return "D";
    } else {
        return "F";
    }
}

// Test edge case
console.log(calculateGrade(90));
console.log(calculateGrade(85));
console.log(calculateGrade(75));
console.log(calculateGrade(65));
console.log(calculateGrade(55));''',
                'bugs': ['Actually works correctly - no bug present'],
                'fixed_code': '''function calculateGrade(score) {
    if (score >= 90) {
        return "A";
    } else if (score >= 80) {
        return "B";
    } else if (score >= 70) {
        return "C";
    } else if (score >= 60) {
        return "D";
    } else {
        return "F";
    }
}

// Test edge case
console.log(calculateGrade(90));
console.log(calculateGrade(85));
console.log(calculateGrade(75));
console.log(calculateGrade(65));
console.log(calculateGrade(55));''',
                'description': 'Find the grading system bug!'
            }
        ],
        'java': [
            {
                'code': '''public class AgeChecker {
    public static String checkAge(int age) {
        if (age > 18) {
            return "adult";
        } else if (age > 13) {
            return "teenager";
        } else if (age > 0) {
            return "child";
        } else {
            return "invalid";
        }
    }
    
    public static void main(String[] args) {
        System.out.println(checkAge(25));
        System.out.println(checkAge(16));
        System.out.println(checkAge(8));
        System.out.println(checkAge(18)); // Edge case!
    }
}''',
                'bugs': ['Logic error: age > 18 should be age >= 18 to include 18-year-olds as adults'],
                'fixed_code': '''public class AgeChecker {
    public static String checkAge(int age) {
        if (age >= 18) {
            return "adult";
        } else if (age >= 13) {
            return "teenager";
        } else if (age > 0) {
            return "child";
        } else {
            return "invalid";
        }
    }
    
    public static void main(String[] args) {
        System.out.println(checkAge(25));
        System.out.println(checkAge(16));
        System.out.println(checkAge(8));
        System.out.println(checkAge(18)); // Edge case!
    }
}''',
                'description': 'Fix the age classification logic!'
            },
            {
                'code': '''public class NumberChecker {
    public static String checkNumber(int num) {
        if (num > 0) {
            return "positive";
        } else if (num < 0) {
            return "negative";
        } else {
            return "zero";
        }
    }
    
    public static void main(String[] args) {
        System.out.println(checkNumber(5));
        System.out.println(checkNumber(-3));
        System.out.println(checkNumber(0));
    }
}''',
                'bugs': ['Actually works correctly - no bug present'],
                'fixed_code': '''public class NumberChecker {
    public static String checkNumber(int num) {
        if (num > 0) {
            return "positive";
        } else if (num < 0) {
            return "negative";
        } else {
            return "zero";
        }
    }
    
    public static void main(String[] args) {
        System.out.println(checkNumber(5));
        System.out.println(checkNumber(-3));
        System.out.println(checkNumber(0));
    }
}''',
                'description': 'Find the number classification bug!'
            }
        ]
    },
    'medium': {
        'python': [
            {
                'code': '''def binary_search(arr, target):
    left = 0
    right = len(arr)
    
    while left < right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

# Test
numbers = [1, 3, 5, 7, 9, 11]
print(binary_search(numbers, 7))''',
                'bugs': ['Off-by-one error: right should be len(arr) - 1, and condition should be left <= right'],
                'fixed_code': '''def binary_search(arr, target):
    left = 0
    right = len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

# Test
numbers = [1, 3, 5, 7, 9, 11]
print(binary_search(numbers, 7))''',
                'description': 'Classic off-by-one error in binary search!'
            }
        ],
        'javascript': [
            {
                'code': '''function debounce(func, delay) {
    let timeoutId;
    return function() {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(func, delay);
    };
}

const debouncedLog = debounce(() => {
    console.log("Hello World!");
}, 1000);

debouncedLog();''',
                'bugs': ['Lost context - should preserve "this" and arguments'],
                'fixed_code': '''function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        const context = this;
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(context, args), delay);
    };
}

const debouncedLog = debounce(() => {
    console.log("Hello World!");
}, 1000);

debouncedLog();''',
                'description': 'The debounce function loses context and arguments!'
            }
        ],
        'java': [
            {
                'code': '''public class BinarySearch {
    public static int search(int[] arr, int target) {
        int left = 0;
        int right = arr.length;
        
        while (left < right) {
            int mid = (left + right) / 2;
            if (arr[mid] == target) {
                return mid;
            } else if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        return -1;
    }
    
    public static void main(String[] args) {
        int[] numbers = {1, 3, 5, 7, 9, 11};
        System.out.println(search(numbers, 7));
    }
}''',
                'bugs': ['Off-by-one error: right should be arr.length - 1, condition should be left <= right'],
                'fixed_code': '''public class BinarySearch {
    public static int search(int[] arr, int target) {
        int left = 0;
        int right = arr.length - 1;
        
        while (left <= right) {
            int mid = (left + right) / 2;
            if (arr[mid] == target) {
                return mid;
            } else if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }
        return -1;
    }
    
    public static void main(String[] args) {
        int[] numbers = {1, 3, 5, 7, 9, 11};
        System.out.println(search(numbers, 7));
    }
}''',
                'description': 'Classic off-by-one error in binary search!'
            },
            {
                'code': '''import java.util.HashMap;
import java.util.Map;

public class Cache {
    private Map<String, String> cache = new HashMap<>();
    
    public String get(String key) {
        return cache.get(key);
    }
    
    public void put(String key, String value) {
        cache.put(key, value);
    }
    
    public static void main(String[] args) {
        Cache cache = new Cache();
        cache.put("user1", "John");
        System.out.println(cache.get("user1"));
        System.out.println(cache.get("user2"));
    }
}''',
                'bugs': ['No null check - get() returns null for missing keys without handling'],
                'fixed_code': '''import java.util.HashMap;
import java.util.Map;

public class Cache {
    private Map<String, String> cache = new HashMap<>();
    
    public String get(String key) {
        String value = cache.get(key);
        return value != null ? value : "Key not found";
    }
    
    public void put(String key, String value) {
        if (key != null && value != null) {
            cache.put(key, value);
        }
    }
    
    public static void main(String[] args) {
        Cache cache = new Cache();
        cache.put("user1", "John");
        System.out.println(cache.get("user1"));
        System.out.println(cache.get("user2"));
    }
}''',
                'description': 'Missing null checks can cause issues!'
            }
        ]
    },
    'hard': {
        'python': [
            {
                'code': '''class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance
    
    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return True
        return False
    
    def transfer(self, other_account, amount):
        if self.withdraw(amount):
            other_account.balance += amount
            return True
        return False

# Concurrent access simulation
account1 = BankAccount(1000)
account2 = BankAccount(500)
account1.transfer(account2, 600)''',
                'bugs': ['Race condition - not thread-safe, balance can be corrupted in concurrent access'],
                'fixed_code': '''import threading

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance
        self._lock = threading.Lock()
    
    def withdraw(self, amount):
        with self._lock:
            if amount <= self.balance:
                self.balance -= amount
                return True
            return False
    
    def transfer(self, other_account, amount):
        # Acquire locks in consistent order to prevent deadlock
        first_lock = self._lock if id(self) < id(other_account) else other_account._lock
        second_lock = other_account._lock if id(self) < id(other_account) else self._lock
        
        with first_lock:
            with second_lock:
                if amount <= self.balance:
                    self.balance -= amount
                    other_account.balance += amount
                    return True
                return False

# Concurrent access simulation
account1 = BankAccount(1000)
account2 = BankAccount(500)
account1.transfer(account2, 600)''',
                'description': 'Race condition nightmare - find the concurrency bug!'
            }
        ],
        'javascript': [
            {
                'code': '''async function fetchUserData(userId) {
    const response = await fetch(`/api/users/${userId}`);
    const userData = await response.json();
    return userData;
}

async function processUsers(userIds) {
    const results = [];
    for (const userId of userIds) {
        const userData = await fetchUserData(userId);
        results.push(userData);
    }
    return results;
}

// Usage
processUsers([1, 2, 3, 4, 5]).then(console.log);''',
                'bugs': ['Sequential processing instead of parallel - should use Promise.all for better performance'],
                'fixed_code': '''async function fetchUserData(userId) {
    const response = await fetch(`/api/users/${userId}`);
    if (!response.ok) {
        throw new Error(`Failed to fetch user ${userId}`);
    }
    const userData = await response.json();
    return userData;
}

async function processUsers(userIds) {
    const promises = userIds.map(userId => fetchUserData(userId));
    return await Promise.all(promises);
}

// Usage
processUsers([1, 2, 3, 4, 5]).then(console.log);''',
                'description': 'Performance killer - sequential instead of parallel processing!'
            }
        ],
        'java': [
            {
                'code': '''import java.util.concurrent.ConcurrentHashMap;
import java.util.Map;

public class Counter {
    private Map<String, Integer> counts = new ConcurrentHashMap<>();
    
    public void increment(String key) {
        Integer current = counts.get(key);
        if (current == null) {
            counts.put(key, 1);
        } else {
            counts.put(key, current + 1);
        }
    }
    
    public int getCount(String key) {
        Integer count = counts.get(key);
        return count != null ? count : 0;
    }
    
    public static void main(String[] args) {
        Counter counter = new Counter();
        counter.increment("clicks");
        counter.increment("clicks");
        System.out.println(counter.getCount("clicks"));
    }
}''',
                'bugs': ['Race condition - increment operation is not atomic despite using ConcurrentHashMap'],
                'fixed_code': '''import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.Map;

public class Counter {
    private Map<String, AtomicInteger> counts = new ConcurrentHashMap<>();
    
    public void increment(String key) {
        counts.computeIfAbsent(key, k -> new AtomicInteger(0)).incrementAndGet();
    }
    
    public int getCount(String key) {
        AtomicInteger count = counts.get(key);
        return count != null ? count.get() : 0;
    }
    
    public static void main(String[] args) {
        Counter counter = new Counter();
        counter.increment("clicks");
        counter.increment("clicks");
        System.out.println(counter.getCount("clicks"));
    }
}''',
                'description': 'Race condition in concurrent counter!'
            },
            {
                'code': '''import java.util.*;
import java.util.stream.Collectors;

public class DataProcessor {
    public static List<String> processData(List<String> data) {
        return data.stream()
            .filter(s -> s != null)
            .map(s -> s.toUpperCase())
            .collect(Collectors.toList());
    }
    
    public static void main(String[] args) {
        List<String> data = Arrays.asList("hello", null, "world", "java");
        List<String> result = processData(data);
        
        // Memory leak - keeping reference to large data
        for (int i = 0; i < 1000000; i++) {
            List<String> temp = new ArrayList<>(data);
            temp.add("item" + i);
        }
        
        System.out.println(result);
    }
}''',
                'bugs': ['Memory leak - creating many temporary lists without cleanup, inefficient object creation'],
                'fixed_code': '''import java.util.*;
import java.util.stream.Collectors;

public class DataProcessor {
    public static List<String> processData(List<String> data) {
        return data.stream()
            .filter(Objects::nonNull)
            .map(String::toUpperCase)
            .collect(Collectors.toList());
    }
    
    public static void main(String[] args) {
        List<String> data = Arrays.asList("hello", null, "world", "java");
        List<String> result = processData(data);
        
        // Fixed: Process data efficiently without memory leaks
        System.out.println("Processed " + data.size() + " items");
        System.out.println(result);
    }
}''',
                'description': 'Memory leak and performance issues!'
            }
        ]
    }
}

def get_random_challenge(level, language):
    """Get a random code challenge for the specified level and language"""
    challenges = BUG_HUNT_LEVELS.get(level, {}).get(language, [])
    if challenges:
        return random.choice(challenges)
    return None

def check_bug_fix(user_code, expected_fix, level):
    """Check if user's fix is correct (simplified check)"""
    # Remove whitespace and normalize for comparison
    user_normalized = re.sub(r'\s+', ' ', user_code.strip().lower())
    expected_normalized = re.sub(r'\s+', ' ', expected_fix.strip().lower())
    
    # For easy level, be more lenient
    if level == 'easy':
        # Python fixes
        if 'age >= 0' in user_normalized:  # Age validation fix
            return True
        if 'is_student:' in user_normalized:  # Discount function fix
            return True
        
        # JavaScript fixes  
        if 'length >= 8' in user_normalized and 'length >= 6' in user_normalized:  # Password fix
            return True
        
        # Java fixes
        if 'age >= 18' in user_normalized:  # Age checker fix
            return True
        
        # Check for "no bug" recognition
        if 'no bug' in user_normalized or 'correct' in user_normalized or 'works fine' in user_normalized:
            return True
    
    # Medium level specific fixes
    if level == 'medium':
        # Binary search fixes
        if 'right = len(arr) - 1' in user_normalized and 'left <= right' in user_normalized:
            return True
        if 'right = arr.length - 1' in user_normalized and 'left <= right' in user_normalized:
            return True
        # Debounce fixes
        if '...args' in user_normalized and 'func.apply' in user_normalized:
            return True
        # Cache/null fixes
        if '!= null' in user_normalized or 'null check' in user_normalized:
            return True
    
    # Hard level specific fixes  
    if level == 'hard':
        # Concurrency fixes
        if 'atomicinteger' in user_normalized or 'computeifabsent' in user_normalized:
            return True
        if 'synchronized' in user_normalized or 'lock' in user_normalized:
            return True
        # Promise.all fixes
        if 'promise.all' in user_normalized:
            return True
        # Memory leak fixes
        if 'objects::nonnull' in user_normalized or 'string::touppercase' in user_normalized:
            return True
    
    # For all levels, check similarity with more lenient thresholds
    if level == 'easy':
        similarity_threshold = 0.3  # Very lenient for easy
    elif level == 'medium':
        similarity_threshold = 0.5  # More lenient for medium
    else:
        similarity_threshold = 0.6  # More lenient for hard
    
    # Simple similarity check (in real app, use more sophisticated comparison)
    common_words = set(user_normalized.split()) & set(expected_normalized.split())
    similarity = len(common_words) / max(len(expected_normalized.split()), 1)
    
    return similarity >= similarity_threshold

def simulate_ai_time(level):
    """Simulate realistic AI processing time based on difficulty"""
    # More realistic AI times - humans can actually compete!
    base_times = {'easy': 25, 'medium': 35, 'hard': 60}
    variation = random.uniform(0.8, 1.2)
    return base_times[level] * variation

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/game')
def game_page():
    return render_template('game.html')

@app.route('/learn')
def learn_page():
    return render_template('learn.html')

@app.route('/how-it-works')
def how_it_works():
    return render_template('how_it_works.html')

@app.route('/get-challenge', methods=['POST'])
def get_challenge():
    data = request.get_json()
    level = data.get('level', 'easy')
    language = data.get('language', 'python')
    
    challenge = get_random_challenge(level, language)
    if not challenge:
        return jsonify({'error': 'No challenges available for this level/language'}), 400
    
    ai_time = simulate_ai_time(level)
    time_limits = {'easy': 60, 'medium': 90, 'hard': 120}
    time_limit = time_limits.get(level, 60)
    
    # Generate unique challenge ID and store the challenge
    challenge_id = random.randint(1000, 9999)
    active_challenges[challenge_id] = challenge
    
    return jsonify({
        'code': challenge['code'],
        'description': challenge['description'],
        'bugs': challenge['bugs'],
        'hint': challenge.get('hint', ''),
        'level': level,
        'language': language,
        'ai_time': ai_time,
        'time_limit': time_limit,
        'challenge_id': challenge_id
    })

@app.route('/submit-fix', methods=['POST'])
def submit_fix():
    data = request.get_json()
    user_code = data.get('user_code', '')
    level = data.get('level', 'easy')
    language = data.get('language', 'python')
    user_time = data.get('user_time', 20)
    challenge_id = data.get('challenge_id')
    
    # Get the exact challenge that was played
    challenge = active_challenges.get(challenge_id)
    if not challenge:
        return jsonify({'error': 'Challenge not found or expired'}), 400
    
    # Check if user's fix is correct
    is_correct = check_bug_fix(user_code, challenge['fixed_code'], level)
    
    # Simulate AI time
    ai_time = simulate_ai_time(level)
    
    # Determine winner with level-based time limits
    time_limits = {'easy': 60, 'medium': 90, 'hard': 120}
    time_limit = time_limits.get(level, 60)
    
    if is_correct and user_time < time_limit:
        if user_time < ai_time:
            winner = 'human'
            message = f'🎉 HUMAN WINS! You fixed the bug in {user_time:.1f} seconds! The AI took {ai_time:.1f} seconds.'
        else:
            winner = 'ai'
            message = f'🤖 AI WINS! The AI found the bug in {ai_time:.1f} seconds. You took {user_time:.1f} seconds.'
    elif is_correct:
        winner = 'ai'
        message = f'⏰ TIME\'S UP! You found the bug but took too long. AI wins with {ai_time:.1f} seconds!'
    else:
        winner = 'ai'
        message = f'🤖 AI WINS! The AI found the bug in {ai_time:.1f} seconds. Better luck next time!'
    
    # Clean up the used challenge
    if challenge_id in active_challenges:
        del active_challenges[challenge_id]
    
    return jsonify({
        'winner': winner,
        'message': message,
        'is_correct': is_correct,
        'user_time': user_time,
        'ai_time': ai_time,
        'correct_fix': challenge['fixed_code'],
        'bugs_found': challenge['bugs']
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
