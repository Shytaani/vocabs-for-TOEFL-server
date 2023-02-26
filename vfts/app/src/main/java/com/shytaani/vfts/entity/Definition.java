package com.shytaani.vfts.entity;

import org.apache.ibatis.type.Alias;

@Alias("Definition")
public record Definition(
        Integer id,
        Integer wordId,
        String definition
) {
}
