package com.zbw;

import com.zbw.domain.Department;
import com.zbw.domain.User;
import com.zbw.domain.Vo.BookVo;
import com.zbw.domain.Vo.BorrowingBooksVo;
import com.zbw.mapper.BookCategoryMapper;
import com.zbw.mapper.BorrowingBooksMapper;
import com.zbw.mapper.UserMapper;
import com.zbw.service.IBookService;
import com.zbw.service.IBorrowingBooksRecordService;
import com.zbw.service.IUserService;
import com.zbw.utils.page.Page;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.transaction.annotation.Transactional;

import javax.annotation.Resource;
import java.util.List;

import static org.junit.Assert.*;

@RunWith(SpringRunner.class)
@SpringBootTest
@Transactional
public class DetailedBusinessTest {

    @Resource
    private IUserService userService;

    @Resource
    private IBookService bookService;

    @Resource
    private IBorrowingBooksRecordService borrowingBooksRecordService;

    @Resource
    private UserMapper userMapper;

    @Resource
    private BookCategoryMapper bookCategoryMapper;

    @Resource
    private BorrowingBooksMapper borrowingBooksMapper;

    @Test
    public void userLoginWithCorrectPasswordReturnsUser() {
        User user = userService.userLogin("user1", "123456");

        assertNotNull(user);
        assertEquals(Integer.valueOf(1), user.getUserId());
        assertEquals("user1", user.getUserName());
    }

    @Test
    public void userLoginWithWrongPasswordReturnsNull() {
        User user = userService.userLogin("user1", "wrong-password");

        assertNull(user);
    }

    @Test
    public void findUserByNameReturnsMatchedUserOnly() {
        List<User> users = userService.findUserByUserName("yxc");

        assertEquals(1, users.size());
        assertEquals(Integer.valueOf(2), users.get(0).getUserId());
        assertEquals("yxc", users.get(0).getUserName());
    }

    @Test
    public void findAllDepartmentsReturnsSeededDepartments() {
        List<Department> departments = userService.findAllDepts();

        assertEquals(2, departments.size());
        assertEquals("信息工程学院", departments.get(0).getDeptName());
        assertEquals("电子工程学院", departments.get(1).getDeptName());
    }

    @Test
    public void findUserPageReturnsPageMetadataAndUsers() {
        Page<User> page = userService.findUserByPage(1);

        assertEquals(1, page.getPageNum());
        assertEquals(10, page.getPageSize());
        assertEquals(1, page.getPageCount());
        assertEquals(3, page.getList().size());
    }

    @Test
    public void bookCategoryMapperReturnsPagedCategoriesAndTotalCount() {
        assertEquals(3, bookCategoryMapper.selectAllCount());
        assertEquals(2, bookCategoryMapper.selectByPageNum(0, 2).size());
    }

    @Test
    public void searchBorrowedBookByNameMarksItUnavailable() {
        List<BookVo> books = bookService.selectBooksByBookPartInfo("平凡的世界");

        assertEquals(1, books.size());
        assertEquals(Integer.valueOf(1), books.get(0).getBookId());
        assertEquals("平凡的世界", books.get(0).getBookName());
        assertEquals("不可借", books.get(0).getIsExist());
    }

    @Test
    public void searchAvailableBookByNameMarksItAvailable() {
        List<BookVo> books = bookService.selectBooksByBookPartInfo("数据库系统");

        assertEquals(1, books.size());
        assertEquals(Integer.valueOf(3), books.get(0).getBookId());
        assertEquals("数据库系统", books.get(0).getBookName());
        assertEquals("可借", books.get(0).getIsExist());
    }

    @Test
    public void findBooksByCategoryReturnsPageMetadataAndBookState() {
        Page<BookVo> page = bookService.findBooksByCategoryId(2, 1);

        assertEquals(1, page.getPageNum());
        assertEquals(10, page.getPageSize());
        assertEquals(1, page.getPageCount());
        assertEquals(2, page.getList().size());
        assertEquals("Java程序设计", page.getList().get(0).getBookName());
        assertEquals("不可借", page.getList().get(0).getIsExist());
        assertEquals("数据库系统", page.getList().get(1).getBookName());
        assertEquals("可借", page.getList().get(1).getIsExist());
    }

    @Test
    public void emptyBookCategoryReturnsEmptyPageList() {
        Page<BookVo> page = bookService.findBooksByCategoryId(99, 1);

        assertEquals(1, page.getPageNum());
        assertEquals(1, page.getPageCount());
        assertTrue(page.getList().isEmpty());
    }

    @Test
    public void borrowingRecordPageAssemblesUserBookAndDates() {
        Page<BorrowingBooksVo> page = borrowingBooksRecordService.selectAllByPage(1);

        assertEquals(1, page.getPageNum());
        assertEquals(10, page.getPageSize());
        assertEquals(1, page.getPageCount());
        assertEquals(2, page.getList().size());
        assertEquals("user1", page.getList().get(0).getUser().getUserName());
        assertEquals("平凡的世界", page.getList().get(0).getBook().getBookName());
        assertEquals("2026-06-01", page.getList().get(0).getDateOfBorrowing());
        assertEquals("2026-08-01", page.getList().get(0).getDateOfReturn());
    }

    @Test
    public void userBorrowingAvailableBookCreatesRecordAndPreventsDuplicateBorrowing() {
        MockHttpServletRequest request = new MockHttpServletRequest();
        request.getSession().setAttribute("user", userMapper.selectByPrimaryKey(3));

        assertEquals(2, borrowingBooksMapper.selectAll());
        assertTrue(userService.userBorrowingBook(3, request));
        assertEquals(3, borrowingBooksMapper.selectAll());
        assertFalse(userService.userBorrowingBook(3, request));
    }

    @Test
    public void userReturnBookDeletesOnlyCurrentUsersBorrowingRecord() {
        MockHttpServletRequest request = new MockHttpServletRequest();
        request.getSession().setAttribute("user", userMapper.selectByPrimaryKey(1));

        assertEquals(1, borrowingBooksMapper.selectAllRecordCount(1));
        assertTrue(userService.userReturnBook(1, request));
        assertEquals(0, borrowingBooksMapper.selectAllRecordCount(1));
        assertFalse(userService.userReturnBook(1, request));
    }
}
