	.file	"bubbleSort.c"
	.section	.text.unlikely,"ax",@progbits
.LCOLDB0:
	.text
.LHOTB0:
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
.LCOLDE0:
	.text
.LHOTE0:
	.section	.text.unlikely
.LCOLDB1:
	.text
.LHOTB1:
	.p2align 4,,15
	.globl	bubbleSort
	.type	bubbleSort, @function
bubbleSort:
.LFB24:
	.cfi_startproc
	leal	-1(%rsi), %edx
	testl	%edx, %edx
	jle	.L2
	.p2align 4,,10
	.p2align 3
.L4:
	subl	$1, %edx
	movq	%rdi, %rax
	leaq	4(%rdi,%rdx,4), %rsi
	movq	%rdx, %r8
	.p2align 4,,10
	.p2align 3
.L6:
	movl	(%rax), %edx
	movl	4(%rax), %ecx
	cmpl	%ecx, %edx
	jle	.L5
	movl	%ecx, (%rax)
	movl	%edx, 4(%rax)
.L5:
	addq	$4, %rax
	cmpq	%rsi, %rax
	jne	.L6
	testl	%r8d, %r8d
	movl	%r8d, %edx
	jne	.L4
.L2:
	rep ret
	.cfi_endproc
.LFE24:
	.size	bubbleSort, .-bubbleSort
	.section	.text.unlikely
.LCOLDE1:
	.text
.LHOTE1:
	.section	.text.unlikely
.LCOLDB4:
	.text
.LHOTB4:
	.p2align 4,,15
	.globl	fill_array
	.type	fill_array, @function
fill_array:
.LFB25:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	pushq	%rbx
	.cfi_def_cfa_offset 24
	.cfi_offset 3, -24
	subq	$24, %rsp
	.cfi_def_cfa_offset 48
	testl	%esi, %esi
	jne	.L13
	leaq	400(%rdi), %rbp
	movq	%rdi, %rbx
	.p2align 4,,10
	.p2align 3
.L14:
	xorl	%eax, %eax
	addq	$4, %rbx
	call	rand
	movl	%eax, -4(%rbx)
	cmpq	%rbp, %rbx
	jne	.L14
.L21:
	addq	$24, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 24
	xorl	%eax, %eax
	popq	%rbx
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_def_cfa_offset 8
	ret
	.p2align 4,,10
	.p2align 3
.L13:
	.cfi_restore_state
	movq	%rdi, %rax
	andl	$15, %eax
	shrq	$2, %rax
	negq	%rax
	andl	$3, %eax
	je	.L22
	cmpl	$1, %eax
	movl	$0, (%rdi)
	je	.L23
	cmpl	$3, %eax
	movl	$1, 4(%rdi)
	jne	.L24
	movl	$2, 8(%rdi)
	movl	$97, %r8d
	movl	$3, %esi
.L16:
	movl	$100, %r9d
	movl	%eax, %edx
	movl	$96, %r10d
	subl	%eax, %r9d
	movl	$24, %ecx
.L15:
	movl	%esi, 12(%rsp)
	leaq	(%rdi,%rdx,4), %rdx
	xorl	%eax, %eax
	movd	12(%rsp), %xmm2
	movdqa	.LC3(%rip), %xmm1
	pshufd	$0, %xmm2, %xmm0
	paddd	.LC2(%rip), %xmm0
	.p2align 4,,10
	.p2align 3
.L17:
	addl	$1, %eax
	addq	$16, %rdx
	movaps	%xmm0, -16(%rdx)
	paddd	%xmm1, %xmm0
	cmpl	%ecx, %eax
	jb	.L17
	movl	%r8d, %edx
	leal	(%r10,%rsi), %eax
	subl	%r10d, %edx
	cmpl	%r10d, %r9d
	je	.L21
	movslq	%eax, %rcx
	cmpl	$1, %edx
	movl	%eax, (%rdi,%rcx,4)
	leal	1(%rax), %ecx
	je	.L21
	movslq	%ecx, %rsi
	addl	$2, %eax
	cmpl	$2, %edx
	movl	%ecx, (%rdi,%rsi,4)
	je	.L21
	movslq	%eax, %rdx
	movl	%eax, (%rdi,%rdx,4)
	addq	$24, %rsp
	.cfi_remember_state
	.cfi_def_cfa_offset 24
	xorl	%eax, %eax
	popq	%rbx
	.cfi_def_cfa_offset 16
	popq	%rbp
	.cfi_def_cfa_offset 8
	ret
.L22:
	.cfi_restore_state
	movl	$100, %r10d
	movl	$25, %ecx
	movl	$100, %r9d
	xorl	%edx, %edx
	movl	$100, %r8d
	xorl	%esi, %esi
	jmp	.L15
.L24:
	movl	$98, %r8d
	movl	$2, %esi
	jmp	.L16
.L23:
	movl	$99, %r8d
	movl	$1, %esi
	jmp	.L16
	.cfi_endproc
.LFE25:
	.size	fill_array, .-fill_array
	.section	.text.unlikely
.LCOLDE4:
	.text
.LHOTE4:
	.section	.text.unlikely
.LCOLDB5:
	.section	.text.startup,"ax",@progbits
.LHOTB5:
	.p2align 4,,15
	.globl	main
	.type	main, @function
main:
.LFB26:
	.cfi_startproc
	pushq	%r12
	.cfi_def_cfa_offset 16
	.cfi_offset 12, -16
	pushq	%rbp
	.cfi_def_cfa_offset 24
	.cfi_offset 6, -24
	movl	$400, %edi
	pushq	%rbx
	.cfi_def_cfa_offset 32
	.cfi_offset 3, -32
	xorl	%ebx, %ebx
	call	malloc
	movslq	%eax, %r12
	movq	%r12, %rbp
	.p2align 4,,10
	.p2align 3
.L35:
	xorl	%eax, %eax
	addq	$4, %rbx
	call	rand
	movl	%eax, -4(%rbx,%rbp)
	cmpq	$400, %rbx
	jne	.L35
	movq	%r12, %rdi
	movl	$100, %esi
	call	bubbleSort
	popq	%rbx
	.cfi_def_cfa_offset 24
	xorl	%eax, %eax
	popq	%rbp
	.cfi_def_cfa_offset 16
	popq	%r12
	.cfi_def_cfa_offset 8
	ret
	.cfi_endproc
.LFE26:
	.size	main, .-main
	.section	.text.unlikely
.LCOLDE5:
	.section	.text.startup
.LHOTE5:
	.section	.rodata.cst16,"aM",@progbits,16
	.align 16
.LC2:
	.long	0
	.long	1
	.long	2
	.long	3
	.align 16
.LC3:
	.long	4
	.long	4
	.long	4
	.long	4
	.ident	"GCC: (Ubuntu 5.4.0-6ubuntu1~16.04.10) 5.4.0 20160609"
	.section	.note.GNU-stack,"",@progbits
