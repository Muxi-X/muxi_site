(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
/**
 * navigation for users page
 *
 * Powered by litejs
 */
'use strict';

var index = (function appear() {

	var btn = document.querySelector(".btn");
	var pop = document.querySelector(".pop");
	var cancel = document.querySelector(".cancel");

	var click_on = btn.addEventListener('click', function () {

		pop.className = pop.className.replace(/hide/, ' ');
		pop.className += ' appear ';
	});
	var click_off = cancel.addEventListener('click', function () {

		pop.className = pop.className.replace(/appear/, ' ');
		pop.className += ' hide ';
	});

	return {
		click_on: click_on,
		click_off: click_off
	};
})();
index.click_on();

},{}]},{},[1]);
