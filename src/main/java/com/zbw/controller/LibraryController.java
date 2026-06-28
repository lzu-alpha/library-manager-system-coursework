package com.zbw.controller;

import com.zbw.domain.Admin;
import com.zbw.domain.Book;
import com.zbw.domain.BookCategory;
import com.zbw.domain.User;
import com.zbw.domain.Vo.BookVo;
import com.zbw.domain.Vo.BorrowingBooksVo;
import com.zbw.service.IAdminService;
import com.zbw.service.IBookCategoryService;
import com.zbw.service.IBookService;
import com.zbw.service.IBorrowingBooksRecordService;
import com.zbw.service.IUserService;
import com.zbw.utils.export.CsvExportUtil;
import com.zbw.utils.page.Page;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import javax.annotation.Resource;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.List;

@Controller
public class LibraryController {

    @Resource
    private IAdminService adminService;

    @Resource
    private IUserService userService;

    @Resource
    private IBookService bookService;

    @Resource
    private IBookCategoryService bookCategoryService;

    @Resource
    private IBorrowingBooksRecordService borrowingBooksRecordService;

    @GetMapping({"/", "/index"})
    public String index() {
        return "index";
    }

    @PostMapping("/userLogin")
    public String userLogin(@RequestParam("userName") String userName,
                            @RequestParam("password") String password,
                            HttpServletRequest request) {
        User user = userService.userLogin(userName, password);
        if (user == null) {
            request.getSession().setAttribute("flag", true);
            return "redirect:/";
        }
        request.getSession().setAttribute("flag", false);
        request.getSession().setAttribute("user", user);
        return "redirect:/userIndexPage";
    }

    @PostMapping("/adminLogin")
    public String adminLogin(@RequestParam("userName") String adminName,
                             @RequestParam("password") String password,
                             HttpServletRequest request) {
        Admin admin = adminService.adminLogin(adminName, password);
        if (admin == null) {
            request.getSession().setAttribute("flag", true);
            return "redirect:/";
        }
        request.getSession().setAttribute("flag", false);
        request.getSession().setAttribute("admin", admin);
        return "redirect:/adminIndexPage";
    }

    @GetMapping("/userLogOut")
    public String userLogOut(HttpServletRequest request) {
        request.getSession().removeAttribute("user");
        return "redirect:/";
    }

    @GetMapping("/adminLogOut")
    public String adminLogOut(HttpServletRequest request) {
        request.getSession().removeAttribute("admin");
        return "redirect:/";
    }

    @GetMapping("/adminIndexPage")
    public String adminIndexPage() {
        return "admin/index";
    }

    @GetMapping("/addBookPage")
    public String addBookPage() {
        return "admin/addBook";
    }

    @GetMapping("/addCategoryPage")
    public String addCategoryPage(@RequestParam(value = "pageNum", defaultValue = "1") int pageNum, Model model) {
        model.addAttribute("page", bookCategoryService.selectBookCategoryByPageNum(normalizePageNum(pageNum)));
        return "admin/addCategory";
    }

    @GetMapping("/showBooksPage")
    public String showBooksPage(Model model) {
        model.addAttribute("page", emptyBookPage());
        model.addAttribute("bookCategory", 0);
        return "admin/showBooks";
    }

    @GetMapping("/showBooksResultPageByCategoryId")
    public String showBooksResultPageByCategoryId(@RequestParam("bookCategory") int bookCategory,
                                                  @RequestParam(value = "pageNum", defaultValue = "1") int pageNum,
                                                  Model model) {
        model.addAttribute("page", bookService.findBooksByCategoryId(bookCategory, normalizePageNum(pageNum)));
        model.addAttribute("bookCategory", bookCategory);
        return "admin/showBooks";
    }

    @GetMapping("/showUsersPage")
    public String showUsersPage(@RequestParam(value = "pageNum", defaultValue = "1") int pageNum, Model model) {
        model.addAttribute("page", userService.findUserByPage(normalizePageNum(pageNum)));
        return "admin/showUsers";
    }

    @GetMapping("/addUserPage")
    public String addUserPage() {
        return "admin/addUser";
    }

    @GetMapping("/allBorrowBooksRecordPage")
    public String allBorrowBooksRecordPage(@RequestParam(value = "pageNum", defaultValue = "1") int pageNum, Model model) {
        model.addAttribute("page", borrowingBooksRecordService.selectAllByPage(normalizePageNum(pageNum)));
        return "admin/allBorrowingBooksRecord";
    }

    @GetMapping("/adminInfoPage")
    public String adminInfoPage() {
        return "admin/adminInfo";
    }

    @GetMapping("/userIndexPage")
    public String userIndexPage() {
        return "user/index";
    }

    @GetMapping("/userBorrowBookRecord")
    public String userBorrowBookRecord(HttpServletRequest request, Model model) {
        model.addAttribute("borrowingBooksList", userService.findAllBorrowingBooks(request));
        return "user/borrowingBooksRecord";
    }

    @GetMapping("/borrowingPage")
    public String borrowingPage() {
        return "user/borrowingBooks";
    }

    @GetMapping("/userReturnBooksPage")
    public String userReturnBooksPage() {
        return "user/returnBooks";
    }

    @GetMapping("/findBookPage")
    public String findBookPage(Model model) {
        model.addAttribute("bookList", new ArrayList<BookVo>());
        return "user/findBook";
    }

    @GetMapping("/findBookByBookPartInfo")
    public String findBookByBookPartInfo(@RequestParam(value = "bookPartInfo", defaultValue = "") String bookPartInfo, Model model) {
        model.addAttribute("bookList", bookService.selectBooksByBookPartInfo(bookPartInfo));
        return "user/findBook";
    }

    @GetMapping("/userMessagePage")
    public String userMessagePage() {
        return "user/userMessage";
    }

    @PostMapping("/addBook")
    @ResponseBody
    public boolean addBook(@ModelAttribute Book book) {
        return adminService.addBook(book);
    }

    @PostMapping("/findAllBookCategory")
    @ResponseBody
    public List<BookCategory> findAllBookCategory() {
        return adminService.getBookCategories();
    }

    @PostMapping("/addBookCategory")
    @ResponseBody
    public boolean addBookCategory(@ModelAttribute BookCategory bookCategory) {
        return adminService.addBookCategory(bookCategory);
    }

    @PostMapping("/deleteCategory")
    @ResponseBody
    public boolean deleteCategory(@RequestParam("bookCategoryId") int bookCategoryId) {
        return bookCategoryService.deleteBookCategoryById(bookCategoryId) > 0;
    }

    @PostMapping("/addUser")
    @ResponseBody
    public boolean addUser(@ModelAttribute User user) {
        return userService.insertUser(user) > 0;
    }

    @PostMapping("/deleteUser")
    @ResponseBody
    public boolean deleteUser(@RequestParam("userId") int userId) {
        return userService.deleteUserById(userId) > 0;
    }

    @PostMapping("/updateAdmin")
    @ResponseBody
    public boolean updateAdmin(@ModelAttribute Admin admin, HttpServletRequest request) {
        return adminService.updateAdmin(admin, request);
    }

    @PostMapping("/updateUser")
    @ResponseBody
    public boolean updateUser(@ModelAttribute User user,
                              @RequestParam(value = "UserEmail", required = false) String userEmail,
                              HttpServletRequest request) {
        if (userEmail != null) {
            user.setUserEmail(userEmail);
        }
        return userService.updateUser(user, request);
    }

    @PostMapping("/userBorrowingBook")
    @ResponseBody
    public boolean userBorrowingBook(@RequestParam("bookId") int bookId, HttpServletRequest request) {
        return userService.userBorrowingBook(bookId, request);
    }

    @PostMapping("/userReturnBook")
    @ResponseBody
    public boolean userReturnBook(@RequestParam("bookId") int bookId, HttpServletRequest request) {
        return userService.userReturnBook(bookId, request);
    }

    @GetMapping("/exportBooks")
    public void exportBooks(@RequestParam(value = "bookPartInfo", defaultValue = "") String bookPartInfo,
                            HttpServletResponse response) throws IOException {
        String csv = CsvExportUtil.exportBooks(bookService.selectBooksByBookPartInfo(bookPartInfo));
        writeCsv(response, "books.csv", csv);
    }

    @GetMapping("/exportBorrowingRecords")
    public void exportBorrowingRecords(@RequestParam(value = "pageNum", defaultValue = "1") int pageNum,
                                       HttpServletResponse response) throws IOException {
        Page<BorrowingBooksVo> page = borrowingBooksRecordService.selectAllByPage(normalizePageNum(pageNum));
        List<BorrowingBooksVo> records = page == null ? new ArrayList<BorrowingBooksVo>() : page.getList();
        String csv = CsvExportUtil.exportBorrowingRecords(records);
        writeCsv(response, "borrowing-records.csv", csv);
    }

    private int normalizePageNum(int pageNum) {
        return Math.max(pageNum, 1);
    }

    private Page<BookVo> emptyBookPage() {
        Page<BookVo> page = new Page<>();
        page.setList(new ArrayList<BookVo>());
        page.setPageNum(1);
        page.setPageSize(10);
        page.setPageCount(1);
        return page;
    }

    private void writeCsv(HttpServletResponse response, String fileName, String csv) throws IOException {
        response.setCharacterEncoding(StandardCharsets.UTF_8.name());
        response.setContentType("text/csv;charset=UTF-8");
        response.setHeader("Content-Disposition", "attachment; filename=" + fileName);
        response.getWriter().write('\ufeff');
        response.getWriter().write(csv);
    }
}
