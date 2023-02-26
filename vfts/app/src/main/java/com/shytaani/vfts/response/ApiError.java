package com.shytaani.vfts.response;

import java.util.List;
import java.util.ArrayList;

public record ApiError(String message, List<Detail> details) {

    public ApiError(String message) {
        this(message, new ArrayList<Detail>());
    }

    void addDetails(String field, String message) {
        details.add(new Detail(field, message));
    }

    private record Detail(String field, String message) {
    }
}
