package com.shytaani.vfts.service;

import java.util.List;

import org.springframework.stereotype.Service;

import com.shytaani.vfts.dao.CardMapper;
import com.shytaani.vfts.dto.Card;
import com.shytaani.vfts.entity.Word;

@Service
public class VftsService {

    private final CardMapper mapper;
    
    public VftsService(CardMapper mapper) {
        this.mapper = mapper;
    }

    public List<Card> getCards() {
        List<Word> words = mapper.findWords();
        return words.stream().map(word -> {
            List<String> definitions = mapper.findDefinitions(word.id())
                .stream()
                .map(definition -> definition.definition())
                .toList();
            List<String> sentences = mapper.findSentences(word.id())
                .stream()
                .map(sentence -> sentence.sentence())
                .toList();
            return new Card(word.id(), word.word(), definitions, sentences);
        }).toList();
    }

    public Card getCard(int id) {
        Word word = mapper.findWord(id).orElseThrow();
        List<String> definitions = mapper.findDefinitions(word.id())
            .stream()
            .map(definition -> definition.definition())
            .toList();
        List<String> sentences = mapper.findSentences(word.id())
            .stream()
            .map(sentence -> sentence.sentence())
            .toList();
        return new Card(word.id(), word.word(), definitions, sentences);
    }
}
