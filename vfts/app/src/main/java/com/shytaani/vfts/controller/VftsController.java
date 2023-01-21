package com.shytaani.vfts.controller;

import java.util.List;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.shytaani.vfts.dto.Card;
import com.shytaani.vfts.service.VftsService;

@RestController
@RequestMapping("/v1")
public class VftsController {
    
    private final VftsService service;

    public VftsController(VftsService service) {
        this.service = service;
    }

    @GetMapping("/cards")
    public List<Card> getCards() {
        return service.getCards();
    }

    @GetMapping("/card/{id}")
    public Card getCard(@PathVariable Integer id) {
        return service.getCard(id);
    }
}
