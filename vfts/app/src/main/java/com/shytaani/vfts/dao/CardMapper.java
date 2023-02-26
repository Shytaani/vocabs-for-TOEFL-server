package com.shytaani.vfts.dao;

import java.util.List;
import java.util.Optional;

import org.apache.ibatis.annotations.Mapper;

import com.shytaani.vfts.entity.Definition;
import com.shytaani.vfts.entity.Sentence;
import com.shytaani.vfts.entity.Word;

@Mapper
public interface CardMapper {
    
    List<Word> findWords();

    Optional<Word> findWord(int id);

    List<Definition> findDefinitions(int wordId);

    List<Sentence> findSentences(int wordId);
}
