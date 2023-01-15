package com.shytaani.vfts.entity;

import org.apache.ibatis.type.Alias;

@Alias("Sentence")
public record Sentence(
        Integer id,
        Integer wordId,
        String sentence
) {
}
