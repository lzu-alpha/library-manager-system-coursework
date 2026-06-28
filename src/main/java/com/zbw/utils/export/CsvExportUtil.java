package com.zbw.utils.export;

import com.zbw.domain.Book;
import com.zbw.domain.User;
import com.zbw.domain.Vo.BookVo;
import com.zbw.domain.Vo.BorrowingBooksVo;

import java.util.List;

public final class CsvExportUtil {

    private CsvExportUtil() {
    }

    public static String exportBooks(List<BookVo> books) {
        StringBuilder csv = new StringBuilder();
        appendRow(csv, "bookId", "bookName", "bookAuthor", "bookPublish", "isExist");
        if (books == null) {
            return csv.toString();
        }
        for (BookVo book : books) {
            appendRow(csv,
                    valueOf(book == null ? null : book.getBookId()),
                    valueOf(book == null ? null : book.getBookName()),
                    valueOf(book == null ? null : book.getBookAuthor()),
                    valueOf(book == null ? null : book.getBookPublish()),
                    valueOf(book == null ? null : book.getIsExist()));
        }
        return csv.toString();
    }

    public static String exportBorrowingRecords(List<BorrowingBooksVo> records) {
        StringBuilder csv = new StringBuilder();
        appendRow(csv, "userId", "userName", "bookId", "bookName", "dateOfBorrowing", "dateOfReturn");
        if (records == null) {
            return csv.toString();
        }
        for (BorrowingBooksVo record : records) {
            User user = record == null ? null : record.getUser();
            Book book = record == null ? null : record.getBook();
            appendRow(csv,
                    valueOf(user == null ? null : user.getUserId()),
                    valueOf(user == null ? null : user.getUserName()),
                    valueOf(book == null ? null : book.getBookId()),
                    valueOf(book == null ? null : book.getBookName()),
                    valueOf(record == null ? null : record.getDateOfBorrowing()),
                    valueOf(record == null ? null : record.getDateOfReturn()));
        }
        return csv.toString();
    }

    private static void appendRow(StringBuilder csv, String... values) {
        for (int i = 0; i < values.length; i++) {
            if (i > 0) {
                csv.append(',');
            }
            csv.append(escape(values[i]));
        }
        csv.append(System.lineSeparator());
    }

    private static String escape(String value) {
        if (value == null) {
            return "";
        }
        boolean shouldQuote = value.contains(",")
                || value.contains("\"")
                || value.contains("\n")
                || value.contains("\r");
        String escaped = value.replace("\"", "\"\"");
        return shouldQuote ? "\"" + escaped + "\"" : escaped;
    }

    private static String valueOf(Object value) {
        return value == null ? "" : String.valueOf(value);
    }
}
