package com.shytaani.vfts.dto;

import java.util.List;

public record Card(
    int id,
    String word,
    List<String> definitions,
    List<String> sentences
    ) {
}
