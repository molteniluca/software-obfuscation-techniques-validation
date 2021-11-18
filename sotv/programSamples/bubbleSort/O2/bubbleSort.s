	.file	"bubbleSort.c"
	.section	.text.unlikely,"ax",@progbits
.LCOLDB0:
	.text
.LHOTB0:
	.p2align 4,,15
	.type	fill_array.part.0, @function
fill_array.part.0:
.LFB27:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	pushq	%rbx
	.cfi_def_cfa_offset 24
	.cfi_offset 3, -24
	leaq	400(%rdi), %rbp
	movq	%rdi, %rbx
	subq	$8, %rsp
	.cfi_def_cfa_offset 32
	.p2align 4,,10
	.p2align 3
.L2:
	xorl	%eax, %eax
	addq	$4, %rbx
	call	rand
	movl	%eax, -4(%rbx)
	cmpq	%rbp, %rbx
	jne	.L2
	addq	$8, %rsp
	.cfi_def_cfa_offset 24
	popq	%rbx
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE27:
	.size	fill_array.part.0, .-fill_array.part.0
	.section	.text.unlikely
.LCOLDE0:
	.text
.LHOTE0:
	.section	.text.unlikely
.LCOLDB1:
	.text
.LHOTB1:
	.p2align 4,,15
	.globl	swap
	.type	swap, @function
swap:
.LFB23:
	.cfi_startproc
	movl	(%rdi), %eax
	movl	(%rsi), %edx
	movl	%edx, (%rdi)
	movl	%eax, (%rsi)
	ret
	.cfi_endproc
.LFE23:
	.size	swap, .-swap
	.section	.text.unlikely
.LCOLDE1:
	.text
.LHOTE1:
	.section	.text.unlikely
.LCOLDB2:
	.text
.LHOTB2:
	.p2align 4,,15
	.globl	bubbleSort
	.type	bubbleSort, @function
bubbleSort:
.LFB24:
	.cfi_startproc
	leal	-1(%rsi), %edx
	testl	%edx, %edx
	jle	.L7
	.p2align 4,,10
	.p2align 3
.L9:
	subl	$1, %edx
	movq	%rdi, %rax
	leaq	4(%rdi,%rdx,4), %rsi
	movq	%rdx, %r8
	.p2align 4,,10
	.p2align 3
.L11:
	movl	(%rax), %edx
	movl	4(%rax), %ecx
	cmpl	%ecx, %edx
	jle	.L10
	movl	%ecx, (%rax)
	movl	%edx, 4(%rax)
.L10:
	addq	$4, %rax
	cmpq	%rsi, %rax
	jne	.L11
	testl	%r8d, %r8d
	movl	%r8d, %edx
	jne	.L9
.L7:
	rep ret
	.cfi_endproc
.LFE24:
	.size	bubbleSort, .-bubbleSort
	.section	.text.unlikely
.LCOLDE2:
	.text
.LHOTE2:
	.section	.text.unlikely
.LCOLDB3:
	.text
.LHOTB3:
	.p2align 4,,15
	.globl	fill_array
	.type	fill_array, @function
fill_array:
.LFB25:
	.cfi_startproc
	testl	%esi, %esi
	jne	.L17
	jmp	fill_array.part.0
	.p2align 4,,10
	.p2align 3
.L17:
	xorl	%eax, %eax
	.p2align 4,,10
	.p2align 3
.L18:
	movl	%eax, (%rdi,%rax,4)
	addq	$1, %rax
	cmpq	$100, %rax
	jne	.L18
	rep ret
	.cfi_endproc
.LFE25:
	.size	fill_array, .-fill_array
	.section	.text.unlikely
.LCOLDE3:
	.text
.LHOTE3:
	.section	.text.unlikely
.LCOLDB4:
	.section	.text.startup,"ax",@progbits
.LHOTB4:
	.p2align 4,,15
	.globl	main
	.type	main, @function
main:
.LFB26:
	.cfi_startproc
	pushq	%rbx
	.cfi_def_cfa_offset 16
	.cfi_offset 3, -16
	movl	$400, %edi
	call	malloc
	movslq	%eax, %rbx
	movq	%rbx, %rdi
	call	fill_array.part.0
	movq	%rbx, %rdi
	movl	$100, %esi
	call	bubbleSort
	xorl	%eax, %eax
	popq	%rbx
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE26:
	.size	main, .-main
	.section	.text.unlikely
.LCOLDE4:
	.section	.text.startup
.LHOTE4:
	.ident	"GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.10) 5.4.0 20160609"
	.section	.note.GNU-stack,"",@progbits
