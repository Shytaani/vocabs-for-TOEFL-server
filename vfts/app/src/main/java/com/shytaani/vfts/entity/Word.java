package com.shytaani.vfts.entity;

import org.apache.ibatis.type.Alias;

@Alias("Word")
public record Word(
        Integer id,
        String word
) {
}
