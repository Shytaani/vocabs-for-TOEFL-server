package com.shytaani.vfts.handler;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.context.request.WebRequest;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;

import com.shytaani.vfts.exception.NoSuchCardException;
import com.shytaani.vfts.response.ApiError;

@RestControllerAdvice("com.shytaani.vfts.controller")
public class VftsExceptionHandler extends ResponseEntityExceptionHandler {

    @ExceptionHandler(NoSuchCardException.class)
    public ResponseEntity<ApiError> handleNoSuchCardException(NoSuchCardException ex, WebRequest request) {
        var apiError = new ApiError(ex.getMessage());
        return new ResponseEntity<>(apiError, HttpStatus.NOT_FOUND);
    }
}
