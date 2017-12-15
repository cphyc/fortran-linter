;;; flycheck-fortran-linter.el --- Help to have compliant fortran

;; Copyright (C) 2017 Corentin Cadiou

;; Author: Corentin Cadiou <corentin.cadiou@cphyc.me>
;; URL: https://github.com/cphyc/fortran-syntax
;; Version: 1.0.1
;; Keywords: flycheck, fortran, fortran90
;; Package-Requires: ((flycheck))

;; This file is not part of GNU Emacs.

;; This program is free software; you can redistribute it and/or modify
;; it under the terms of the GNU General Public License as published by
;; the Free Software Foundation, either version 3 of the License, or
;; (at your option) any later version.

;; This program is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;; GNU General Public License for more details.

;; You should have received a copy of the GNU General Public License
;; along with this program.  If not, see <http://www.gnu.org/licenses/>.

;;; Commentary:

;; This is extension for Flycheck.

;;;; Setup

;; (eval-after-load 'flycheck
;;   '(progn
;;      (require 'flycheck-fortran-linter)
;;      ;; Add Fortran linter
;;      (flycheck-add-next-checker 'fortran/fortran-gfortran `append)))

;;; Code:

(require 'flycheck)

(flycheck-def-option-var flycheck-fortran-linter-linelength "80" fortran-linter
  "The allowed line length for Fortran linter.

linelength=digits
  This is the allowed line length for the project. The default value is
  80 characters.

  Examples:
    --linelength=120"
  :type '(string :tag "Line length")
  :safe #'stringp
  :package-version '(flycheck . "0.18"))

(flycheck-def-option-var flycheck-fortran-linter-max-errors "500" fortran-linter
  "Maximum number of errors to report.

  This is the maximum number of errors the linter will report. The default value is
  500 characters.

  Examples:
    --max-errs=500"
  :type '(string :tag "Max errors")
  :safe #'stringp
  :package-version '(flycheck . "0.18"))


(flycheck-define-checker fortran-linter
  "A Fortran linter.

See URL `https://github.com/cphyc/fortran-syntax'."
  :command ("/home/ccc/.bin/fortran-linter.py"
            "--syntax-only"
            (option "--linelength=" flycheck-fortran-linter-linelength concat)
	    (option "--max-errors=" flycheck-fortran-linter-max-errors concat)
            source)
  :error-patterns
  ((warning line-start (file-name) ":" line (or ":" ".") column (or ": " ":\n")
            (or (= 3 (zero-or-more not-newline) "\n") "")
            "Warning: " (message) line-end))
  :modes (f90-mode))

(add-to-list 'flycheck-checkers 'fortran-linter 'append)

(provide 'flycheck-fortran-linter)

;;; flycheck-fortran-linter.el ends here
