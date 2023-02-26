package com.shytaani.vfts.handler;

import com.shytaani.vfts.exception.NoSuchCardException;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.HttpStatus;
import org.springframework.mock.web.MockHttpServletRequest;
import org.springframework.web.servlet.handler.DispatcherServletWebRequest;

import static org.junit.jupiter.api.Assertions.*;

@SpringBootTest
public class VftsExceptionHandlerTests {

    @Autowired
    private VftsExceptionHandler handler;

    @Test
    public void handleNoSuchCardExceptionReturnsAnErrorResponse() {
        var ex = new NoSuchCardException("test message");
        var req = new DispatcherServletWebRequest(new MockHttpServletRequest());

        var res = handler.handleNoSuchCardException(ex, req);

        assertAll(() -> {
            assertEquals(ex.getMessage(), res.getBody().message());
            assertEquals(HttpStatus.NOT_FOUND, res.getStatusCode());
        });

    }
}
