package com.zbw;

import com.zbw.domain.Book;
import com.zbw.domain.User;
import com.zbw.domain.Vo.BookVo;
import com.zbw.domain.Vo.BorrowingBooksVo;
import com.zbw.utils.export.CsvExportUtil;
import org.junit.Test;

import java.util.ArrayList;
import java.util.List;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;

public class CsvExportUtilTest {

    @Test
    public void exportBooksWritesHeaderAndRows() {
        List<BookVo> books = new ArrayList<>();
        BookVo book = new BookVo();
        book.setBookId(1);
        book.setBookName("Database System");
        book.setBookAuthor("Author A");
        book.setBookPublish("Press A");
        book.setIsExist("Available");
        books.add(book);

        String csv = CsvExportUtil.exportBooks(books);

        assertTrue(csv.startsWith("bookId,bookName,bookAuthor,bookPublish,isExist"));
        assertTrue(csv.contains("1,Database System,Author A,Press A,Available"));
    }

    @Test
    public void exportBooksEscapesCommaQuoteAndLineBreak() {
        List<BookVo> books = new ArrayList<>();
        BookVo book = new BookVo();
        book.setBookId(2);
        book.setBookName("Java, Spring");
        book.setBookAuthor("Alice \"A\"");
        book.setBookPublish("Press\r\nB");
        book.setIsExist("Unavailable");
        books.add(book);

        String csv = CsvExportUtil.exportBooks(books);

        assertTrue(csv.contains("\"Java, Spring\""));
        assertTrue(csv.contains("\"Alice \"\"A\"\"\""));
        assertTrue(csv.contains("\"Press\r\nB\""));
    }

    @Test
    public void exportBorrowingRecordsWritesUserBookAndDates() {
        User user = new User();
        user.setUserId(7);
        user.setUserName("reader");

        Book book = new Book();
        book.setBookId(11);
        book.setBookName("Software Engineering");

        BorrowingBooksVo record = new BorrowingBooksVo();
        record.setUser(user);
        record.setBook(book);
        record.setDateOfBorrowing("2026-06-01");
        record.setDateOfReturn("2026-08-01");

        List<BorrowingBooksVo> records = new ArrayList<>();
        records.add(record);

        String csv = CsvExportUtil.exportBorrowingRecords(records);

        assertTrue(csv.startsWith("userId,userName,bookId,bookName,dateOfBorrowing,dateOfReturn"));
        assertTrue(csv.contains("7,reader,11,Software Engineering,2026-06-01,2026-08-01"));
    }

    @Test
    public void exportNullCollectionsWritesOnlyHeader() {
        assertEquals(1, CsvExportUtil.exportBooks(null).split("\\R").length);
        assertEquals(1, CsvExportUtil.exportBorrowingRecords(null).split("\\R").length);
    }
}
