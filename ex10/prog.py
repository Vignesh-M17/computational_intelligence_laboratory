Script started on Mon Apr 20 15:39:02 2026
[23bcs123@mepcolinux ex10]$cat prog1.lisp
(defun fibonacci-series (n)
  "Generates a list of the first N Fibonacci numbers iteratively."
  (loop :for a := 0 :then b
        :and b := 1 :then (+ a b)
        :repeat n
        :collect a))

(format t "Enter the number of Fibonacci elements: ")
(finish-output) ; Ensures the prompt appears immediately

(let ((input (read)))
  (if (numberp input)
      (format t "Series: ~A~%" (fibonacci-series input))
      (format t "Please enter a valid number.~%")))

CL-USER 7 : 2 > (run-fib)
Enter the number of Fibonacci elements: 20
Series (Recursive): (0 1 1 2 3 5 8 13 21 34 55 89 144 233 377 610 987 1597 2584 4181)

CL-USER 8 : 2 > (run-fib)
Enter the number of Fibonacci elements: 10
Series (Recursive): (0 1 1 2 3 5 8 13 21 34)

[23bcs123@mepcolinux ex10]$cat prog2.lisp
(defun is-palindrome (input)
  (let ((clean-input (string-downcase (string input))))
    (equal clean-input (reverse clean-input))))
(defun run-palindrome-check ()
  (format t "~%Enter a word to check: ")
  (finish-output)
  (let ((user-word (read-line)))
    (if (is-palindrome user-word)
        (format t "Yes! '~A' is a palindrome.~%" user-word)
        (format t "No, '~A' is not a palindrome.~%" user-word)))
  (values))

CL-USER 3 : 2 > (run-palindrome-check)

Enter a word to check: vikki
No, 'vikki' is not a palindrome.

CL-USER 4 : 2 > (run-palindrome-check)

Enter a word to check: malayalam
Yes! 'malayalam' is a palindrome.

[23bcs123@mepcolinux ex10]$cat prog3.lisp
(defun area-of-circle (radius)
  (* pi (expt radius 2)))
(defun run-circle-calc ()
  (format t "~%Enter the radius: ")
  (finish-output)
  (let ((r (read)))
    (format t "The area is: ~,2F~%" (area-of-circle r)))
  (values))

CL-USER 5 : 2 > (run-circle-calc)

Enter the radius: 8
The area is: 201.06

CL-USER 6 : 2 > (run-circle-calc)

Enter the radius: 5
The area is: 78.54

[23bcs123@mepcolinux ex10]$exit

Script done on Mon Apr 20 15:39:05 2026