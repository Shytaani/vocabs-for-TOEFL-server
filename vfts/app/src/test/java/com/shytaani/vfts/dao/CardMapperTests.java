package com.shytaani.vfts.dao;

import com.shytaani.vfts.entity.Definition;
import com.shytaani.vfts.entity.Sentence;
import com.shytaani.vfts.entity.Word;

import org.junit.jupiter.api.Test;
import org.mybatis.spring.boot.test.autoconfigure.MybatisTest;
import org.springframework.beans.factory.annotation.Autowired;
import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertDoesNotThrow;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

@MybatisTest
public class CardMapperTests {

    @Autowired
    private CardMapper mapper;

    @Test
    void testFindWords() {
        List<Word> words = mapper.findWords();
        assertTrue(words.size() > 0);
    }

    @Test
    void testFindWord() {
        Optional<Word> opt = mapper.findWord(1);
        assertDoesNotThrow(() -> opt.orElseThrow());
        assertAll(() -> {
            Word word = opt.get();
            assertNotEquals(null, word);
            assertEquals("Abundant", word.word());
        });
    }

    @Test
    void testFindDefinitions() {
        List<Definition> definitions = mapper.findDefinitions(1);
        assertTrue(definitions.size() > 0);
        assertAll(() -> {
            assertEquals(1, definitions.get(0).id());
            assertEquals("Present in large quantities.", definitions.get(0).definition());
        });
    }

    @Test
    void testFindSentences() {
        List<Sentence> sentences = mapper.findSentences(1);
        assertTrue(sentences.size() > 0);
        assertAll(() -> {
            assertEquals(1, sentences.get(0).id());
            assertEquals("Living close to a lake means we have an abundant supply of water.", sentences.get(0).sentence());
        });
    }
}
