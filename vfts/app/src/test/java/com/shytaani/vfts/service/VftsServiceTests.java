package com.shytaani.vfts.service;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrowsExactly;
import static org.mockito.Mockito.*;

import java.util.List;
import java.util.Optional;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mock;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.MessageSource;

import com.shytaani.vfts.dao.CardMapper;
import com.shytaani.vfts.dto.Card;
import com.shytaani.vfts.entity.Definition;
import com.shytaani.vfts.entity.Sentence;
import com.shytaani.vfts.entity.Word;
import com.shytaani.vfts.exception.NoSuchCardException;
import org.springframework.context.i18n.LocaleContextHolder;

@SpringBootTest
public class VftsServiceTests {

    private VftsService service;

    @Mock
    private CardMapper mapper;

    @Autowired
    private MessageSource messageSource;

    @BeforeEach
    void init() {

        service = new VftsService(mapper, messageSource);

        when(mapper.findDefinitions(1)).thenReturn(List.of(
            new Definition(1, 1, "def11")
        ));
        when(mapper.findDefinitions(2)).thenReturn(List.of(
            new Definition(3, 2, "def21"),
            new Definition(4, 2, "def22")
        ));
        when(mapper.findSentences(1)).thenReturn(List.of(
            new Sentence(1, 1, "sen11")
        ));
        when(mapper.findSentences(2)).thenReturn(List.of(
            new Sentence(3, 2, "sen21"),
            new Sentence(4, 2, "sen22")
        ));
    }

    @Test
    void getCardsReturnsCardList() {
        when(mapper.findWords()).thenReturn(List.of(
            new Word(1, "word1"),
            new Word(2, "word2")
        ));

        List<Card> cards = service.getCards();

        assertAll(() -> {
            assertEquals(2, cards.size());

            assertEquals("word1", cards.get(0).word());
            assertEquals(1, cards.get(0).definitions().size());
            assertEquals("def11", cards.get(0).definitions().get(0));
            assertEquals(1, cards.get(0).sentences().size());
            assertEquals("sen11", cards.get(0).sentences().get(0));

            assertEquals("word2", cards.get(1).word());
            assertEquals(2, cards.get(1).definitions().size());
            assertEquals("def21", cards.get(1).definitions().get(0));
            assertEquals("def22", cards.get(1).definitions().get(1));
            assertEquals(2, cards.get(1).sentences().size());
            assertEquals("sen21", cards.get(1).sentences().get(0));
            assertEquals("sen22", cards.get(1).sentences().get(1));
        });
    }

    @Test
    void getCardReturnsACard() throws NoSuchCardException {
        when(mapper.findWord(1)).thenReturn(Optional.of(new Word(1, "word1")));
        when(mapper.findWord(2)).thenReturn(Optional.of(new Word(2, "word2")));

        Card card1 = service.getCard(1);
        Card card2 = service.getCard(2);

        assertAll(() -> {
            assertEquals("word1", card1.word());
            assertEquals(1, card1.definitions().size());
            assertEquals("def11", card1.definitions().get(0));
            assertEquals(1, card1.sentences().size());
            assertEquals("sen11", card1.sentences().get(0));
        });

        assertAll(() -> {
            assertEquals("word2", card2.word());
            assertEquals(2, card2.definitions().size());
            assertEquals("def21", card2.definitions().get(0));
            assertEquals("def22", card2.definitions().get(1));
            assertEquals(2, card2.sentences().size());
            assertEquals("sen21", card2.sentences().get(0));
            assertEquals("sen22", card2.sentences().get(1));
        });
    }

    @Test
    void getCardsReturnsEmptyList() {
        when(mapper.findWords()).thenReturn(List.of());

        List<Card> cards = service.getCards();
        
        assertEquals(0, cards.size());
    }

    @Test
    void getCardThrowsNoSuchCardException() {
        when(mapper.findWord(1)).thenReturn(Optional.empty());

        var ex = assertThrowsExactly(NoSuchCardException.class, () -> service.getCard(1));
        assertEquals(messageSource.getMessage("no.such.card", new Integer[]{1}, LocaleContextHolder.getLocale()),
                ex.getMessage());
    }
}
